from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime, func
from wsgiref.handlers import format_date_time

from daily4.db import db_init;
from daily4.db.db_base import DBBase
from daily4.models import Base

import numpy as np

class iResult(Base, DBBase):
    __tablename__ = 'results'
    db = db_init();
    
    draw_id=Column(Integer,primary_key=True,autoincrement=False)
    date_time=Column(DateTime)
    r=Column(Integer)
    
    def __init__(self, DrawID=0, DrawDateTime='', Pick=0):
        self.draw_id=DrawID;
        self.date_time = str(DrawDateTime);
        self.r = int(Pick);
        
        super().setupDBBase(iResult, iResult.draw_id, self.draw_id)
        
    def setup(self):
        res = self.db.session.query(iResult).filter(iResult.draw_id==self.draw_id).first();
        if (res is not None):
            self.date_time=res.date_time;        
            self.r=res.r
    
    def getPick(self):
        return self.r;
    
    def setPick(self, pick):
        self.r=pick

    def get_dict(self):
        dict={};
        dict[self.draw_id]=np.array([self.date_time, self.r]);
        return dict;
    
    def toString(self):
        return str(self.draw_id)+"["+str(self.date_time)+"]"+ str(self.r)
    
    def getLastDrawID(self):
        #return self.db.session.query(func.max(iResult.draw_id)).scalar();
        return self.db.session.query(iResult).order_by(iResult.draw_id.desc()).first().draw_id;
