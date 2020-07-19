
from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime, func
from wsgiref.handlers import format_date_time

from dailyderby.db import db_init;
from dailyderby.db.db_base import DBBase
from dailyderby.models import Base, iresult

import numpy as np

class iDraw(Base, DBBase):
    __tablename__ = 'draws'
    db = db_init();
    
    draw_id=Column(Integer,primary_key=True,autoincrement=False)
    p1n1=Column(Integer)
    p1n2=Column(Integer)
    p1n3=Column(Integer)
    p1n4=Column(Integer)
    p1n5=Column(Integer)
    p1n6=Column(Integer)
    p1n7=Column(Integer)
    p1n8=Column(Integer)
    p1n9=Column(Integer)
    p1n10=Column(Integer)
    p1n11=Column(Integer)
    p1n12=Column(Integer)
    p2n1=Column(Integer)
    p2n2=Column(Integer)
    p2n3=Column(Integer)
    p2n4=Column(Integer)
    p2n5=Column(Integer)
    p2n6=Column(Integer)
    p2n7=Column(Integer)
    p2n8=Column(Integer)
    p2n9=Column(Integer)
    p2n10=Column(Integer)
    p2n11=Column(Integer)
    p2n12=Column(Integer)
    p3n1=Column(Integer)
    p3n2=Column(Integer)
    p3n3=Column(Integer)
    p3n4=Column(Integer)
    p3n5=Column(Integer)
    p3n6=Column(Integer)
    p3n7=Column(Integer)
    p3n8=Column(Integer)
    p3n9=Column(Integer)
    p3n10=Column(Integer)
    p3n11=Column(Integer)
    p3n12=Column(Integer)
    
    p1 = 0;
    p2 = 0;
    p3 = 0;
    
    def __init__(self, DrawID=0, PickArray=[0, 0, 0]):
        self.reset();
        self.draw_id=DrawID;
        self.p1 = int(PickArray[0]);
        self.p2 = int(PickArray[1]);
        self.p3 = int(PickArray[2])
        if(PickArray[0]>0):
            self.derive();
        
        super().setupDBBase(iDraw, iDraw.draw_id, self.draw_id)
        
    def reset(self):
        self.draw_id = 0;
        self.p1n1 = 0
        self.p1n2 = 0
        self.p1n3 = 0
        self.p1n4 = 0
        self.p1n5 = 0
        self.p1n6 = 0
        self.p1n7 = 0
        self.p1n8 = 0
        self.p1n9 = 0
        self.p1n10 = 0
        self.p1n11 = 0
        self.p1n12 = 0
        
        self.p2n1 = 0
        self.p2n2 = 0
        self.p2n3 = 0
        self.p2n4 = 0
        self.p2n5 = 0
        self.p2n6 = 0
        self.p2n7 = 0
        self.p2n8 = 0
        self.p2n9 = 0
        self.p2n10 = 0
        self.p2n11 = 0
        self.p2n12 = 0        
        
        self.p3n1 = 0
        self.p3n2 = 0
        self.p3n3 = 0
        self.p3n4 = 0
        self.p3n5 = 0
        self.p3n6 = 0
        self.p3n7 = 0
        self.p3n8 = 0
        self.p3n9 = 0        
        self.p3n10 = 0
        self.p3n11 = 0
        self.p3n12 = 0
        
    def derive(self):        
        self.setDraw(1,self.p1);
        
        self.setDraw(2,self.p2);
        
        self.setDraw(3,self.p3);
        
    def setDraw(self, Place, Number):
        variable = 'p{0}n{1}'.format(str(Place), str(Number));
        setattr(self, variable, 1)
        
    def getDraw(self, Place, Number):
        variable = 'p{0}n{1}'.format(str(Place), str(Number));
        return getattr(self, variable)
    
    def getArray(self):
        lst = list();
        #lst.append(self.draw_id);
        
        p=1
        while p < 4:
            n = 0;
            while n<13:
                lst.append(self.getDraw(p,n))
                n += 1;
            p += 1;
        return lst;
        
    def fromArray(self, drawArray):
        str_pick=''
        idx = 0;
        p = 1;
        while p < 4:
            n = 0;
            while n < 13:
                idx = ((p-1)*12)+n
                if(drawArray[idx] > 0 ):
                    variable= 'p{0}n{1}'.format(str(p),str(n))
                    setattr(self,variable,drawArray[idx])
                    str_pick += str(n)
                n+=1;
            p+=1;
                
        self.pick = int(str_pick)
        
    
    def toString(self):
        Draw='';
        p=1
        while p < 4:
            n = 0;
            while n<13:
                Draw += str(self.getDraw(p,n))
                n += 1;
            p += 1;
            Draw += '\n';
            
        return '[{0}] \n [{1}]'.format(self.draw_id, Draw)
