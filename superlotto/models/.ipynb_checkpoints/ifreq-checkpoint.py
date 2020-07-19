from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from superlotto.db import db_init;
from superlotto.db.db_base import DBBase
from superlotto.models import Base, ipick, iresult

import numpy as np

class iFreq(Base, DBBase):
    __tablename__ = 'freqs'
    db = db_init();
    
    freq_id=Column(Integer,primary_key=True, autoincrement=True)
    freq_score=Column(Integer)
    freq_sample=Column(Integer)
    draw_id=Column(Integer)    
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
    n13=Column(Integer)
    n14=Column(Integer)
    n15=Column(Integer)
    n16=Column(Integer)
    n17=Column(Integer)
    n18=Column(Integer)
    n19=Column(Integer)
    n20=Column(Integer)
    n21=Column(Integer)
    n22=Column(Integer)
    n23=Column(Integer)
    n24=Column(Integer)
    n25=Column(Integer)
    n26=Column(Integer)
    n27=Column(Integer)
    n28=Column(Integer)
    n29=Column(Integer)
    n30=Column(Integer)
    n31=Column(Integer)
    n32=Column(Integer)
    n33=Column(Integer)
    n34=Column(Integer)
    n35=Column(Integer)
    n36=Column(Integer)
    n37=Column(Integer)
    n38=Column(Integer)
    n39=Column(Integer)
    n40=Column(Integer)
    n41=Column(Integer)
    n42=Column(Integer)
    n43=Column(Integer)
    n44=Column(Integer)
    n45=Column(Integer)
    n46=Column(Integer)
    n47=Column(Integer)  
    mega=Column(Integer)
    
    drawDict={0:0}
    
    def __init__(self, DrawID=0):
        self.freq_id = None
        self.draw_id=DrawID
        self.reset()
        if (self.draw_id>0): self.setup()
        
        super().setupDBBase(iFreq, iFreq.freq_id, self.freq_id)
        
    def reset(self):        
        for i in range(48 ):            
            self.drawDict[i]=0;
            if i>0:
                setattr(self, "n"+str(i), 0);
        self.mega = 0;
        
    def set_key_value(self, key, value):
        setattr(self, "n"+str(key), value)
        
    def derive(self):
        return 0;

