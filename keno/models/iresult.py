from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from keno.db import db_init;
from keno.db.db_base import DBBase
from keno.models import Base, ipick

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
    r6=Column(Integer)
    r7=Column(Integer)
    r8=Column(Integer)
    r9=Column(Integer)
    r10=Column(Integer)
    r11=Column(Integer)
    r12=Column(Integer)
    r13=Column(Integer)
    r14=Column(Integer)
    r15=Column(Integer)
    r16=Column(Integer)
    r17=Column(Integer)
    r18=Column(Integer)
    r19=Column(Integer)
    r20=Column(Integer)
    mega=Column(Float)
    
    pick=''
    
    def __init__(self, DrawID=0, DrawDateTime='', PickArray=[0 for x in range(20)], Mega=0):
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
            self.r6=r.r6
            self.r7=r.r7
            self.r8=r.r8
            self.r9=r.r9
            self.r10=r.r10
            self.r11=r.r11
            self.r12=r.r12
            self.r13=r.r13
            self.r14=r.r14
            self.r15=r.r15
            self.r16=r.r16
            self.r17=r.r17
            self.r18=r.r18
            self.r19=r.r19
            self.r20=r.r20
            self.mega=r.mega
            self.pick=ipick.iPick(self.numToArray())
    
    def getPick(self):
        return self.pick;
    
    def setPick(self, pick):
        self.pick=pick
        self.numFromArray(self.pick.getArray())
    
    def numFromArray(self, array20=[0 for x in range(20)]):
        self.r1=array20[0]
        self.r2=array20[1]
        self.r3=array20[2]
        self.r4=array20[3]
        self.r5=array20[4]
        self.r6=array20[5]
        self.r7=array20[6]
        self.r8=array20[7]
        self.r9=array20[8]
        self.r10=array20[9]
        self.r11=array20[10]
        self.r12=array20[11]
        self.r13=array20[12]
        self.r14=array20[13]
        self.r15=array20[14]
        self.r16=array20[15]
        self.r17=array20[16]
        self.r18=array20[17]
        self.r19=array20[18]
        self.r20=array20[19]
        #self.setPick(ipick.iPick(array20))
        
    def numToArray(self):
        numArray=[self.r1, self.r2, self.r3, self.r4, self.r5, self.r6, self.r7, self.r8, self.r9, self.r10, self.r11, self.r12, self.r13, self.r14, self.r15, self.r16, self.r17, self.r18, self.r19, self.r20];
        return numArray
    
    def get_dict(self):
        dict={};
        dict[self.draw_id]=np.array([self.r1, self.r2, self.r3, self.r4, self.r5, self.r6, self.r7, self.r8, self.r9, self.r10, self.r11, self.r12, self.r13, self.r14, self.r15, self.r16, self.r17, self.r18, self.r19, self.r20]);
        return dict;
    
    def toString(self):
        return str(self.draw_id)+"["+str(self.date_time)+"]"+self.pick.toString() +"["+str(self.mega)+"]"
    
    def getLastDrawID(self):
        return self.db.session.query(iResult).order_by(iResult.draw_id.desc()).first().draw_id;
    
