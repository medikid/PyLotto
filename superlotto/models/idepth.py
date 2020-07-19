from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from superlotto.db import db_init;
from superlotto.db.db_base import DBBase
from superlotto.models import Base, ipick, iresult, idraw

import numpy as np

class iDepth(Base, DBBase):
    __tablename__ = 'depths'
    db = db_init();
    
    draw_id=Column(Integer,primary_key=True, autoincrement=False)
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
    
    depthDict={0:0}
    
    def __init__(self, DrawID=0):
        self.draw_id=DrawID
        self.reset()      
        
        super().setupDBBase(iDepth, iDepth.draw_id, self.draw_id)
        
    def reset(self):        
        for i in range(48):            
            self.depthDict[i]=0;
            if i>0:
                setattr(self, "n"+str(i), 0);
        self.mega = 0;
                
    def derive(self):
        if (self.draw_id>0):
            cur_id=self.draw_id;
            prev_id=self.draw_id-1;
            prev_depth=self.db.session.query(iDepth).filter(iDepth.draw_id==prev_id).first();            
            cur_draw=idraw.iDraw(cur_id);
            for i in self.depthDict.keys():
                if i > 0:
                    if getattr(cur_draw, "n"+str(i))==1:
                        setattr(self, "n"+str(i), 0)
                    else:
                        setattr(self, "n"+str(i), getattr(prev_depth, "n"+str(i))+1)
                    
        
    def setup(self):
        d = self.db.session.query(iDepth).filter(iDepth.draw_id==self.draw_id).first();
        if d is not None:
            self.mega=d.mega
            for i in self.depthDict.keys():
                if i > 0:
                    setattr(self, "n"+str(i), getattr(d,"n"+str(i)))
                    
    def get_dict(self):
        dict={};
        dict[self.draw_id]=np.array([self.n1, self.n2, self.n3, self.n4, self.n5, self.n6, self.n7, self.n8, self.n9, self.n10, self.n11, self.n12, self.n13, self.n14, self.n15, self.n16, self.n17, self.n18, self.n19, self.n20, self.n21, self.n22, self.n23, self.n24, self.n25, self.n26, self.n27, self.n28, self.n29, self.n30, self.n31, self.n32, self.n33, self.n34, self.n35, self.n36, self.n37, self.n38, self.n39, self.n40, self.n41, self.n42, self.n43, self.n44, self.n45, self.n46, self.n47])
        return dict;
    
    def toString(self):
        return str(self.get_dict()) + "[" + str(self.mega)+"]"

