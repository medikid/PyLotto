from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean, BigInteger, DECIMAL, VARCHAR
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from hotspot.db import db_init;
from hotspot.db.db_base import DBBase
from hotspot.models import Base, ipick, iresult, ibin, index, iexplore

import numpy as np

class ExploreLog(Base, DBBase):
    __tablename__ = 'explore_logs'
    db = db_init();
    
    xplr_log_id=Column(Integer,primary_key=True, autoincrement=True)
    xplr_id = Column(Integer, ForeignKey("explores.xplr_id"))
    idx_id=Column(Integer)
    draw_id=Column(Integer)
    x_bin0140=Column(BigInteger)
    x_bin4180=Column(BigInteger)
    qualifiers=Column(Integer)
    wins=Column(Integer)
    efficiency = Column(DECIMAL(5,4))

    #my_explore = relationship("iexplore.iExplore", foreign_keys=xplr_id, backref='logs', primaryjoin="iExplore.xplr_id==ExploreLog.xplr_id")
    #my_index = relationship("Index", backref='my_logs')

    array_qualifiers=[]
    
    def __init__(self, xplrID = 0, idxID=0, drawID = 0, ar_qualifiers=[], d_bin0140=0, d_bin4180=0):
        self.xplr_id = xplrID        
        self.idx_id=idxID
        self.draw_id = drawID
        self.array_qualifiers = ar_qualifiers;
        self.qualifiers = len(ar_qualifiers)
        self.set_bin();
        self.validate_qualifiers(d_bin0140, d_bin4180);
        self.calc_efficiency();
        #if (self.label != None or self.idx_id > 0 ) : self.setup()
                
        super().setupDBBase(ExploreLog, ExploreLog.xplr_log_id, self.xplr_log_id)

    

    def set_bin(self):
        b0140 = ibin.iBin(); b4180 = ibin.iBin();
        for i in self.array_qualifiers:
            if i > 40:
                b4180.set_bit(i)
            else: b0140.set_bit(i)
        self.x_bin0140 = b0140.get_bin(); #833831981626 for 2277311
        self.x_bin4180 = b4180.get_bin();  #206435647488 for 2277311

    def validate_qualifiers(self, d_bin0140, d_bin4180):
        self.wins = 0;
        win_1 = d_bin0140 & self.x_bin0140
        win_2 = d_bin4180 & self.x_bin4180
        self.wins += bin(win_1).count("1")
        self.wins += bin(win_2).count("1")
        
    def calc_efficiency(self):
        if self.qualifiers > 0:
            self.efficiency = self.wins / self.qualifiers;
        else: self.efficiency = 0;

    def reset(self):
        self.xplr_log_id=0
        self.xplr_id = 0
        self.idx_id=0
        self.draw_id=0
        self.x_bin0140=0
        self.x_bin4180=0
        self.qualifiers=0
        self.wins=0
        self.efficiency = 0

    #NOT SETUP
    def setup(self):
        d = None;
        if (self.label == None): 
            d = self.db.session.query(index.Index).filter(index.Index.idx_id ==self.idx_id).first();
        else: d = self.db.session.query(index.Index).filter(index.Index.label ==self.label).first();

        if d is not None:            
            self.xplr_log_id= d.xplr_log_id
            self.xplr_id = d.xplr_id
            self.idx_id=d.idx_id
            self.draw_id=d.draw_id
            self.x_bin0140=d.x_bin0140
            self.x_bin4180=d.x_bin4180
            self.qualifiers=d.qualifiers
            self.wins=d.wins
            self.efficiency = d.efficiency