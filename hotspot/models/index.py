from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean, BigInteger, VARCHAR, DECIMAL, Text
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from hotspot.db import db_init;
from hotspot.db.db_base import DBBase
from hotspot.models import Base, ipick, iresult, ibin, iexplore

import numpy as np

class Index(Base, DBBase):
    __tablename__ = 'indexes'
    db = db_init();
     
    idx_id=Column(Integer,primary_key=True, autoincrement=True)
    label=Column(VARCHAR(20))
    desc = Column(Text(1000))
    overall_qualified_draws=Column(Integer)
    overall_qualified_nums=Column(Integer)
    overall_wins = Column(Integer)
    overall_efficiency = Column(DECIMAL(5,4))
    overall_best = Column(Integer)
    overall_worst = Column(Integer)
    overall_avg = Column(DECIMAL(6,4))

    explores = relationship("iExplore", backref='my_index')

    #explores = relationship("iexplore.iExplore", foreign_keys=idx_id, backref='my_index', primary_join="iExplore.idx_id==Index.idx_id")
   

    
    
    def __init__(self, Label = None, Desc = None, idxID=0):
        self.label = Label
        self.desc = Desc
        self.idx_id = idxID
        if (self.label != None or self.idx_id > 0 ) : 
            self.setup()
                
        super().setupDBBase(Index, Index.idx_id, self.idx_id)

    def register(self):
        print("Index.register(): Want to register %s %s" % (self.label, self.desc))
        d = self.db.session.query(Index).filter(Index.label == self.label ).first();
        if (d == None):            
            self.db_save();
            print("Registered index %s %s" %(self.label, self.desc))
        else: print("Index already registered")

    def reset(self):
        print("Resetting Index")
        self.label = None
        self.desc = None
        self.overall_qualified_draws = 0
        self.overall_qualified_nums = 0
        self.overall_wins = 0
        self.overall_efficiency= 0
        self.overall_best= 0
        self.overall_worst= 0
        self.overall_avg = 0

    def setup(self):
        d = None;
        print("Setting up index %s" % self.label)
        if (self.label != None): 
            d = self.db.session.query(Index).filter(Index.label ==self.label).first();
            print("pulling index by label")
        else: 
            d = self.db.session.query(Index).filter(Index.idx_id ==self.idx_id).first();
            print("pulling index by id")

        if d is not None:
            self.idx_id = d.idx_id            
            self.label = d.label
            self.desc = d.desc
            self.overall_qualified_draws = d.overall_qualified_draws
            self.overall_qualified_nums = d.overall_qualified_nums
            self.overall_wins = d.overall_wins
            self.overall_efficiency=d.overall_efficiency
            self.overall_best=d.overall_best
            self.overall_worst=d.overall_worst
            self.overall_avg = d.overall_avg