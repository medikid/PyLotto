from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from hotspot.db import db_init;
from hotspot.db.db_base import DBBase
from hotspot.models import Base, ipick, iresult, idraw

import numpy as np

class iTicket(Base, DBBase):
    __tablename__ = 'tickets'
    db = db_init();
    
    tick_id=Column(Integer,primary_key=True, autoincrement=True)    
    draw_id=Column(Integer)
    picks_total=Column(Integer)
    opt_x=Column(Boolean)
    strat_id=Column(String)
    session_id=Column(Integer)
    t1=Column(Integer)
    t2=Column(Integer)
    t3=Column(Integer)
    t4=Column(Integer)
    t5=Column(Integer)
    t6=Column(Integer)
    t7=Column(Integer)
    t8=Column(Integer)
    t9=Column(Integer)
    t10=Column(Integer)
    t11=Column(Integer)
    t12=Column(Integer)
    t13=Column(Integer)
    t14=Column(Integer)
    t15=Column(Integer)
    t16=Column(Integer)
    t17=Column(Integer)
    t18=Column(Integer)
    t19=Column(Integer)
    t20=Column(Integer)
    t21=Column(Integer)
    t22=Column(Integer)
    t23=Column(Integer)
    t24=Column(Integer)
    t25=Column(Integer)
    t26=Column(Integer)
    t27=Column(Integer)
    t28=Column(Integer)
    t29=Column(Integer)
    t30=Column(Integer)
    t31=Column(Integer)
    t32=Column(Integer)
    t33=Column(Integer)
    t34=Column(Integer)
    t35=Column(Integer)
    t36=Column(Integer)
    t37=Column(Integer)
    t38=Column(Integer)
    t39=Column(Integer)
    t40=Column(Integer)
    t41=Column(Integer)
    t42=Column(Integer)
    t43=Column(Integer)
    t44=Column(Integer)
    t45=Column(Integer)
    t46=Column(Integer)
    t47=Column(Integer)
    t48=Column(Integer)
    t49=Column(Integer)
    t50=Column(Integer)
    t51=Column(Integer)
    t52=Column(Integer)
    t53=Column(Integer)
    t54=Column(Integer)
    t55=Column(Integer)
    t56=Column(Integer)
    t57=Column(Integer)
    t58=Column(Integer)
    t59=Column(Integer)
    t60=Column(Integer)
    t61=Column(Integer)
    t62=Column(Integer)
    t63=Column(Integer)
    t64=Column(Integer)
    t65=Column(Integer)
    t66=Column(Integer)
    t67=Column(Integer)
    t68=Column(Integer)
    t69=Column(Integer)
    t70=Column(Integer)
    t71=Column(Integer)
    t72=Column(Integer)
    t73=Column(Integer)
    t74=Column(Integer)
    t75=Column(Integer)
    t76=Column(Integer)
    t77=Column(Integer)
    t78=Column(Integer)
    t79=Column(Integer)
    t80=Column(Integer)
    
    tx=Column(Integer)
    t_bin=Column(Bit)
    tx_bin=Column(Bit)
    t_matches=Column(Integer)
    tx_match=Column(Boolean)
    t_prize=Column(Integer)
    
    tickDict={0:0}
    
    def __init__(self, DrawID=0):
        self.tick_id=0;
        self.draw_id=DrawID;
        self.reset()
        if (self.tick_id>0): self.setup()
        
        super().setupDBBase(iTicket, iTicket.tick_id, self.tick_id)
        
    def reset(self):        
        for i in range(81):            
            self.tickDict[i]=0;
            if i>0:
                setattr(self, "t"+str(i), 0);
        self.tx = 0;
                
    def derive(self):
        if (self.draw_id>0):
            self.reset()
            r = iresult.iResult(self.draw_id);
            r.setup(); #setup from db
            self.mega=r.mega
            for x in r.pick.getArray():
                setattr(self,"n"+str(x),1)
                self.drawDict[x]=1 
        
    def setup(self):
        d = self.db.session.query(iTicket).filter(iTicket.tick_id==self.tick_id).first();
        if d is not None:
            for i in self.tickDict.keys():
                if (i>0):
                    setattr(self, "t"+str(i), getattr(d,"t"+str(i)) )
                    self.drawDict[i]=getattr(self, "t"+str(i))
        
    def toString(self):
        return str(self.get_dict())  + "[" + str(self.tx)+"]"
            
            
    def get_dict(self):
        dict={};
        dict[self.tick_id]=np.array([self.t1, self.t2, self.t3, self.t4, self.t5, self.t6, self.t7, self.t8, self.t9, self.t10, self.t11, self.t12, self.t13, self.t14, self.t15, self.t16, self.t17, self.t18, self.t19, self.t20, self.t21, self.t22, self.t23, self.t24, self.t25, self.t26, self.t27, self.t28, self.t29, self.t30, self.t31, self.t32, self.t33, self.t34, self.t35, self.t36, self.t37, self.t38, self.t39, self.t40, self.t41, self.t42, self.t43, self.t44, self.t45, self.t46, self.t47, self.t48, self.t49, self.t50, self.t51, self.t52, self.t53, self.t54, self.t55, self.t56, self.t57, self.t58, self.t59, self.t60, self.t61, self.t62, self.t63, self.t64, self.t65, self.t66, self.t67, self.t68, self.t69, self.t70, self.t71, self.t72, self.t73, self.t74, self.t75, self.t76, self.t77, self.t78, self.t79, self.t80]);
        return dict;