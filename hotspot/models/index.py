from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean, BigInteger, VARCHAR, DECIMAL, Text
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from hotspot.db import db_init;
from hotspot.db.db_base import DBBase
from hotspot.models import Base, ipick, iresult, ibin

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

    
    
    def __init__(self, Label = None, idxID=0):
        self.idx_id=idxID
        self.label = Label
        if (self.label != None or self.idx_id > 0 ) : 
            self.setup()
                
        super().setupDBBase(Index, Index.idx_id, self.idx_id)

    def register(self, Label = None, Desc = None):
        d = self.db.session.query(Index).filter(Index.label == Label ).first();
        if (d == None):
            self.reset;
            self.label = Label;
            self.desc = Desc;

            self.db_save;
        else: print("Index already registered")

    def reset(self):
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
        if (self.label == None): 
            d = self.db.session.query(Index).filter(Index.idx_id ==self.idx_id).first();
        else: d = self.db.session.query(Index).filter(Index.label ==self.label).first();

        if d is not None:            
            self.label = d.label
            self.desc = d.desc
            self.overall_qualified_draws = d.overall_qualified_draws
            self.overall_qualified_nums = d.overall_qualified_nums
            self.overall_wins = dr.overall_wins
            self.overall_efficiency=d.overall_efficiency
            self.overall_best=d.overall_best
            self.overall_worst=d.overall_worst
            self.overall_avg = d.overall_avg