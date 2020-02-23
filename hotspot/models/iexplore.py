from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean, BigInteger, DECIMAL
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from hotspot.db import db_init;
from hotspot.db.db_base import DBBase
from hotspot.models import Base, ipick, iresult, ibin, index, idraw, idepth, iresult, iexplorelog

from copy import deepcopy

import numpy as np

class Qualifier():
    draw_id=0;
    num=0;
    ball=0;
    win=0;
    
    def __init__(DrawID=0, Num=0, Win=0):
        self.draw_id = DrawID;
        self.num = Num;
        self.ball = "n"+Num;
        self.win = Win;

    def is_win(self, Win=0):
        self.win = Win;

    def toString(self):
        Str = str(self.draw_id())  + "[" + str(self.ball);
        if (self.win == 1):
            Str += " = 1]"
        else: Str += "]";

        return Str;


class iExplore(Base, DBBase):
    __tablename__ = 'explores'
    db = db_init();
    
    xplr_id=Column(Integer,primary_key=True, autoincrement=True)
    idx_id=Column(Integer, ForeignKey("indexes.idx_id"))
    from_draw=Column(Integer)
    to_draw=Column(Integer)
    qualified_draws=Column(Integer)
    qualifiers=Column(Integer)
    win=Column(Integer)
    efficiency=Column(DECIMAL(5,4))
    best=Column(Integer)
    worst=Column(Integer)
    avg=Column(DECIMAL(6,4))

    logs = relationship("iexplorelog.ExploreLog", foreign_keys=xplr_id, backref='my_explore', primaryjoin="ExploreLog.xplr_id==iExplore.xplr_id")
    #my_index = relationship("index.Index", foreign_keys=idx_id, backref='explores')

    _IS_CURRENT=False;
    _INDEX = None#Index();
    _DRAWS={}
    _DEPTHS={}
    _LOGS = []
    _Q_LIST = {}

    LABEL = "NOT SET"
    DESC = "NOT SET"
    
    def __init__(self, Label = None, DrawID=0, Cnt=0, isCurrent=False):
        if (Label != None):
            self.reset();
            self._INDEX = index.Index(Label);
            self.idx_id = self._INDEX.idx_id;            
            self._IS_CURRENT = isCurrent;
            if (isCurrent):
                self.from_draw = DrawID-1;
            else: self.from_draw = DrawID
            self.to_draw = DrawID - Cnt;
            self.load_data()

            print("iExplore initiated for ", Label, DrawID, Cnt)

        super().setupDBBase(iExplore, iExplore.xplr_id, self.xplr_id)
    

    def register_index(self):
        print("iExplore.register_index(): Want to register %s %s" % (self.LABEL, self.DESC))
        self._INDEX = index.Index(self.LABEL, self.DESC);
        self._INDEX.register();


    def load_data(self):
        FROM_DRAW_ID = self.to_draw-1; TO_DRAW_ID = self.from_draw + 1;

        self.load_draws(FROM_DRAW_ID, TO_DRAW_ID);
        self.load_depths(FROM_DRAW_ID, TO_DRAW_ID);
        
        print("Loaded draws/depths from " + str(FROM_DRAW_ID)+"-"+str(TO_DRAW_ID))
            


    def load_draws(self, FROM_DRAW_ID, TO_DRAW_ID):            
        res_draws = self.db.session.query(idraw.iDraw).filter(idraw.iDraw.draw_id >= FROM_DRAW_ID).filter(idraw.iDraw.draw_id <= TO_DRAW_ID).all();
        
        for dr in res_draws :
            self._DRAWS.update(dr.__get_dict__());
            #print(self._DRAWS)


    def load_depths(self, FROM_DRAW_ID, TO_DRAW_ID):        
        res_depths = self.db.session.query(idepth.iDepth).filter(idepth.iDepth.draw_id >= FROM_DRAW_ID).filter(idepth.iDepth.draw_id <= TO_DRAW_ID).all();

        for dp in res_depths:
            self._DEPTHS.update(dp.__get_dict__());
        


    def execute_algo(self, X, Y):
        print("Index algo not defined")

    def validate(self):
        for q in self._Q_LIST:
            if (self._DRAWS[q.draw_id+1][q.ball] == 1):
                q.is_win(1);


    def add_qualifier(self, DrawID, Num, Win=0):
        q = Qualifier(DrawID, Num, Win);
        self._Q_LIST.amend(q);
        self.qualifiers += 1;

    def validate_qualifier(self, DrawID, Num):
        Win = 0;
        if (self._DRAWS[DrawID+1][Num] == 1):
            Win = 1;
        return Win;


    def explore(self, DBSave=True, batch=10):
        cur_draw = self.to_draw;
        last_draw = self.from_draw; #loads data in referse order
        print("Exploring from "+ self.to_draw.__str__() + " to "+ self.from_draw.__str__() )

        while (cur_draw  <= last_draw):
            X = cur_draw; self._Q_LIST[X] = {}
            Y = 1;
            while (Y <= 80):
                if(self.execute_algo(X, Y)):
                    self._Q_LIST[X][Y] = self.validate_qualifier(X, Y);
                Y += 1;
            cur_draw += 1;

        self.finalize_logs();            
        self.finalize_metrics()
        if (DBSave):
                self.save_logs()
        self.print_summary();

    

    def finalize_logs(self):
        self.qualified_draws = len(self._Q_LIST); self.qualifiers = 0; self.win = 0; self.best = 0; self.worst = 0; self.avg = 0;

        
        for dr, q in self._Q_LIST.items(): #loop per draw
            q_per_draw = len(q); win_per_draw = 0; eff_per_draw = 0.0;
            
            xplrlg = iexplorelog.ExploreLog(self.xplr_id, self.idx_id, dr,q,self._DRAWS[dr]['d_bin0140'],self._DRAWS[dr]['d_bin4180']);
            self._LOGS.append(xplrlg);
            
            for x, y in q.items(): #loop per qualifier
                if (y == 1):
                    win_per_draw += 1;
            
            #now finalize per draw
            self.qualifiers += q_per_draw;
            self.win += win_per_draw;
            if (q_per_draw > 0): eff_per_draw = win_per_draw / q_per_draw;
            if (eff_per_draw > self.best): self.best = eff_per_draw;
            if (eff_per_draw < self.worst ): self.worst = eff_per_draw;
            


    def finalize_metrics(self):     
        self.efficiency= self.win / self.qualifiers;


    def save_logs(self):
        self.db_save();

        self.db.session.bulk_save_objects(self._LOGS)
        self.db.session.commit();

    def print_qualifiers(self, result=False):
        if (result):
            for dr, q in self._Q_LIST.items():
                print(dr, q, len(q));
        else: 
            for dr, q in self._Q_LIST.items():
                print(dr, list(q.keys()), len(q));

    def print_summary(self,qualifiers=False, result=False):
        print("################################");
        print("INDEX: %s" % self.LABEL);
        print("EXPLORE DATA: %s-%s" % (self.from_draw, self.to_draw))
        print("Qualified Draws: %s, Efficiency: %s/%s=%s" % (self.qualified_draws, self.win, self.qualifiers, self.efficiency))
        print("Per Draw Best: %s / worst: %s / Avg: %s " % (self.best, self.worst, self.avg))
        if(qualifiers):
            self.print_qualifiers(result);

        print("#################################")
            
    

    def reset(self):
        #self.xplr_id=0
        self.idx_id=0
        self.from_draw=0
        self.to_draw=0
        self.qualified_draws=0
        self.qualifiers=0
        self.win=0
        self.efficiency=0
        self.best=0
        self.worst=0
        self.avg=0

    def setup(self):
        d = None;
        if (self.xplr_id > 0 ): 
            d = self.db.session.query(iExplore).filter(iExplore.xplr_id ==self.xplr_id).first();
        else: d = self.db.session.query(iExplore).filter(iExplore.label ==self.label).first();

        if d is not None:            
            self.xplr_id=d.xplr_id
            self.idx_id=d.idx_id
            self.from_draw=d.from_draw
            self.to_draw=d.to_draw
            self.qualified_draws=d.qualified_draws
            self.qualifiers=d.qualifiers
            self.win=d.win
            self.efficiency=d.efficiency
            self.best=d.best
            self.worst=d.worst
            self.avg=d.avg