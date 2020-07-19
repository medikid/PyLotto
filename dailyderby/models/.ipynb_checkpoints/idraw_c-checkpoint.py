from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime, func
from wsgiref.handlers import format_date_time

from dailyderby.db import db_init;
from dailyderby.db.db_base import DBBase
from dailyderby.models import Base, iresult

import numpy as np

class iDrawC(Base, DBBase):
    __tablename__ = 'draws_c'
    db = db_init();
    
    draw_id=Column(Integer,primary_key=True,autoincrement=False)
    n1=Column(Integer)
    n2=Column(Integer)
    n3=Column(Integer)
    n4=Column(Integer)
    n5=Column(Integer)
    n6=Column(Integer)
    n7=Column(Integer)
    n8=Column(Integer)
    n9=Column(Integer)
    n10=Column(Integer)
    n11=Column(Integer)
    n12=Column(Integer)
    
    pick = 0;
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
        
        super().setupDBBase(iDrawC, iDrawC.draw_id, self.draw_id)
        
    def reset(self):
        self.draw_id = 0;
        self.n1 = 0
        self.n2 = 0
        self.n3 = 0
        self.n4 = 0
        self.n5 = 0
        self.n6 = 0
        self.n7 = 0
        self.n8 = 0
        self.n9 = 0
        self.n10 = 0
        self.n11 = 0
        self.n12 = 0
        
    def derive(self):
        self.setDraw(1,self.p1);
        self.setDraw(2,self.p2);
        self.setDraw(3,self.p3);
        
    def setDraw(self, Place, Number):
        variable = 'n{0}'.format(str(Number));
        setattr(self, variable, 1)
        
    def getDraw(self, Place, Number):
        variable = 'n{0}'.format(str(Number));
        return getattr(self, variable)
    
    def getArray(self):
        lst = list();
        #lst.append(self.draw_id);
        
        p=1
        while p < 4:
            n = 1;
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
            n = 1;
            while n < 13:
                idx = (n-1)
                if(drawArray[idx] > 0 ):
                    variable= 'n{0}'.format(str(p),str(n))
                    setattr(self,variable,drawArray[idx])
                    str_pick += str(n)
                n+=1;
            p+=1;
                
        self.pick = int(str_pick)
        
    
    def toString(self):
        Draw='';
        p=1
        while n<13:
            Draw += str(self.getDraw(p,n))
            n += 1;
            
            Draw += '\n';
            
        return '[{0}] \n [{1}]'.format(self.draw_id, Draw)
