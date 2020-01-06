from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean, BigInteger
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from hotspot.db import db_init;
from hotspot.db.db_base import DBBase
from hotspot.models import Base, ipick, iresult, ibin

import numpy as np

class ExploreLog(Base, DBBase):
    __tablename__ = 'explore_logs'
    db = db_init();
    
    xplr_log_id=Column(Integer,primary_key=True, autoincrement=True)
    xplr_id = Column(Integer)
    idx_id=Column(Integer)
    draw_id=Column(Integer)
    qualifiers=Column(Integer)
    wins=Column(Integer)
    efficiency = Column(DECIMAL(5,4))

    
    
    def __init__(self, label = None, idxID=0):
        self.idx_id=idxID
        if (self.label != None or self.idx_id > 0 ) : self.setup()
                
        super().setupDBBase(ExploreLog, ExploreLog.xplr_log_id, self.xplr_log_id)

    def calc_efficiency(self):
        self.efficiency = self.wins / self.qualifiers;


    def reset(self):
        self.xplr_log_id=0
        self.xplr_id = 0
        self.idx_id=0
        self.draw_id=0
        self.qualifiers=0
        self.wins=0
        self.efficiency = 0

    #NOT SETUP
    def setup(self):
        d = None;
        if (self.label == None): 
            d = self.db.session.query(Index).filter(Index.idx_id ==self.idx_id).first();
        else: d = self.db.session.query(Index).filter(Index.label ==self.label).first();

        if d is not None:            
            self.label = d.label
            self.desc = d.desc
            self.overall_qualified_draws = d.overall_qualified_draws
            self.overall_qualified_nums = d.
            self.overall_wins = overall_wins
            self.overall_efficiency=d.overall_efficiency
            self.overall_best=d.overall_best
            self.overall_worst=d.overall_worst
            self.overall_avg = d.overall_avg