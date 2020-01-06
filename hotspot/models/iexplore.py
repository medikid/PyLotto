from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean, BigInteger, DECIMAL
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from hotspot.db import db_init;
from hotspot.db.db_base import DBBase
from hotspot.models import Base, ipick, iresult, ibin, index, idraw, idepth, iresult



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
    idx_id=Column(Integer)
    from_draw=Column(Integer)
    to_draw=Column(Integer)
    qualified_draws=Column(Integer)
    qualifiers=Column(Integer)
    win=Column(Integer)
    efficiency=Column(DECIMAL(5,4))
    best=Column(Integer)
    worst=Column(Integer)
    avg=Column(DECIMAL(6,4))


    _IS_CURRENT=False;
    _INDEX = {}
    _DRAWS={}
    _DEPTHS={}
    _LOGS = {}
    _Q_LIST = {}
    
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
            self.load()

            print("iExplore initiated for ", Label, DrawID, Cnt)

        super().setupDBBase(iExplore, iExplore.xplr_id, self.xplr_id)


    def load(self):
        FROM_DRAW_ID = self.to_draw-1; TO_DRAW_ID = self.from_draw + 1;
        
        print("Loaded draws/depths from " + str(FROM_DRAW_ID)+"-"+str(TO_DRAW_ID))
            
        res_draws = self.db.session.query(idraw.iDraw).filter(idraw.iDraw.draw_id >= FROM_DRAW_ID).filter(idraw.iDraw.draw_id <= TO_DRAW_ID).all();
        res_depths = self.db.session.query(idepth.iDepth).filter(idepth.iDepth.draw_id >= FROM_DRAW_ID).filter(idepth.iDepth.draw_id <= TO_DRAW_ID).all();

        for dr in res_draws :
            self._DRAWS.update(dr.__get_dict__());
            #print(self._DRAWS)

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
            self.win += 1;
        return Win;


    def explore(self, batch=10):
        cur_draw = self.to_draw;
        last_draw = self.from_draw;
        print("Exploring from "+ self.to_draw.__str__() + " to "+ self.from_draw.__str__() )

        while (cur_draw  <= last_draw):
            X = cur_draw; self._Q_LIST[X] = {}
            Y = 1;
            while (Y <= 80):
                if(self.execute_algo(X, Y)):
                    self.qualifiers += 1;
                    self._Q_LIST[X][Y] = self.validate_qualifier(X, Y);
                Y += 1;
            cur_draw += 1;
            
        self.finalize()

    def finalize(self):        
        self.qualified_draws=len(self._Q_LIST.keys())
        self.efficiency= self.win / self.qualifiers;
        self.best=0
        self.worst=0
        self.avg=0

    def print_qualifiers(self, result=False):
        if (result):
            for dr, q in self._Q_LIST.items():
                print(dr, q, len(q));
        else: 
            for dr, q in self._Q_LIST.items():
                print(dr, list(q.keys()), len(q));

    def print_summary(self,result=False):
        print("################################");
        print("INDEX: %s" % self.LABEL);
        print("EXPLORE DATA: %s-%s" % (self.from_draw, self.to_draw))
        print("Qualified Draws: %s, Efficiency: %s/%s=%s" % (self.qualified_draws, self.win, self.qualifiers, self.efficiency))
        self.print_qualifiers(result);

        print("#################################")
            

        

    def reset(self):
        self.xplr_id=0
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
        if (self.label == None): 
            d = self.db.session.query(Index).filter(Index.idx_id ==self.idx_id).first();
        else: d = self.db.session.query(Index).filter(Index.label ==self.label).first();

        if d is not None:            
            self.label = d.label
            self.desc = d.desc
            self.overall_qualified_draws = d.overall_qualified_draws
            self.overall_qualified_nums = d.overall_qualified_nums
            self.overall_wins = d.overall_wins
            self.overall_efficiency=d.overall_efficiency
            self.overall_best=d.overall_best
            self.overall_worst=d.overall_worst
            self.overall_avg = d.overall_avg