from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime, func
from wsgiref.handlers import format_date_time

from dailyderby.db import db_init;
from dailyderby.db.db_base import DBBase
from dailyderby.models import Base

import numpy as np

class iResult(Base, DBBase):
    __tablename__ = 'results'
    db = db_init();
    
    draw_id=Column(Integer,primary_key=True,autoincrement=False)
    date_time=Column(DateTime)
    r1=Column(Integer)
    r2=Column(Integer)
    r3=Column(Integer)
    rt=Column(String(10))
    i_rt=Column(Integer)
    
    def __init__(self, DrawID=0, DrawDateTime='', PickArray=[1,2,3],RaceTime='',iRaceTime=0):
        self.draw_id=DrawID;
        self.date_time = str(DrawDateTime);
        self.r1 = PickArray[0];
        self.r2 = PickArray[1];
        self.r3 = PickArray[2];
        self.rt = RaceTime;
        self.i_rt = iRaceTime;
        
        super().setupDBBase(iResult, iResult.draw_id, self.draw_id)
        
    def setup(self):
        res = self.db.session.query(iResult).filter(iResult.draw_id==self.draw_id).first();
        if (res is not None):
            self.date_time=res.date_time;        
            self.r1= res.r1
            self.r2 = res.r2;
            self.r3 = res.r3;
            self.rt = res.rt;
            self.i_rt = res.i_rt;
    
    def getPick(self):
        return [self.r1,self.r2,self.r3];
    
    def setPick(self, pickArray):
        self.r1 = PickArray[0];
        self.r2 = PickArray[1];
        self.r3 = PickArray[2];

    def get_dict(self):
        dict={};
        dict[self.draw_id]=np.array([self.date_time, self.r]);
        return dict;
    
    def toString(self):
        return "{0}[{1}][{2}{3}{4}][{5}".format(self.draw_id,self.date_time,self.r1,self.r2,self.r3,self.rt)
    
    def getLastDrawID(self):
        #return self.db.session.query(func.max(iResult.draw_id)).scalar();
        return self.db.session.query(iResult).order_by(iResult.draw_id.desc()).first().draw_id;
