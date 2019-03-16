from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime, func
from wsgiref.handlers import format_date_time

from powerball.db import db_init;
from powerball.db.db_base import DBBase
from powerball.models import Base, ipick

import numpy as np

class iResult(Base, DBBase):
    __tablename__ = 'Results'
    db = db_init();
    
    draw_id=Column(Integer,primary_key=True)
    date_time=Column(DateTime)
    r1=Column(Integer)
    r2=Column(Integer)
    r3=Column(Integer)
    r4=Column(Integer)
    r5=Column(Integer)
    mega=Column(Integer)
    
    pick=''
    
    def __init__(self, DrawID=0, DrawDateTime='', PickArray=[0 for x in range(5)], Mega=0):
        self.draw_id=DrawID
        self.date_time = DrawDateTime
        self.setPick(ipick.iPick(PickArray))
        #self.numFromArray(PickArray)        
        self.mega = Mega;
        
                
        
        super().setupDBBase(iResult, iResult.draw_id, self.draw_id)
        
    def setup(self):
        r = self.db.session.query(iResult).filter(iResult.draw_id==self.draw_id).first();
        if (r is not None):
            self.date_time=r.date_time;        
            self.r1=r.r1
            self.r2=r.r2
            self.r3=r.r3
            self.r4=r.r4
            self.r5=r.r5            
            self.mega=r.mega
            self.pick=ipick.iPick(self.numToArray())
    
    def getPick(self):
        return self.pick;
    
    def setPick(self, pick):
        self.pick=pick
        self.numFromArray(self.pick.getArray())
    
    def numFromArray(self, array20=[0 for x in range(5)]):
        self.r1=array20[0]
        self.r2=array20[1]
        self.r3=array20[2]
        self.r4=array20[3]
        self.r5=array20[4]
        #self.setPick(ipick.iPick(array20))
        
    def numToArray(self):
        numArray=[self.r1, self.r2, self.r3, self.r4, self.r5];
        return numArray
    
    def get_dict(self):
        dict={};
        dict[self.draw_id]=np.array([self.r1, self.r2, self.r3, self.r4, self.r5]);
        return dict;
    
    def toString(self):
        return str(self.draw_id)+"["+str(self.date_time)+"]"+self.pick.toString() +"["+str(self.mega)+"]"
    
    def getLastDrawID(self):
        #return self.db.session.query(func.max(iResult.draw_id)).scalar();
        return self.db.session.query(iResult).order_by(iResult.draw_id.desc()).first().draw_id;
