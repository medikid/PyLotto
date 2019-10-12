from sqlalchemy import Column, Integer, Numeric, String, Text, VARCHAR, DECIMAL, DateTime, Float, Boolean, LargeBinary, Binary, SmallInteger, BigInteger
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from hotspot.db import db_init;
from hotspot.db.db_base import DBBase
from hotspot.models import Base, ipick, iresult, idraw, ibin

import numpy as np
import importlib

class iStrategy(Base, DBBase):
    __tablename__ = 'strategies'
    db = db_init();

    strat_id=Column(VARCHAR(11),primary_key=True, autoincrement=False)
    strategy=Column(VARCHAR(4))
    major_version=Column(SmallInteger)
    minor_version=Column(SmallInteger)
    strat_desc=Column(Text(1000))
    tickets_total=Column(SmallInteger)
    tickets_claimed=Column(Integer)
    cost_total=Column(DECIMAL(11,2))    
    prize_total=Column(DECIMAL(11,2))
    pnl=Column(DECIMAL(11,2))
    match_max=Column(Integer)
    prize_max=Column(DECIMAL(11,2))
    match_min=Column(Integer)
    prize_min=Column(DECIMAL(11,2))
    match_average=Column(Integer)
    prize_average=Column(DECIMAL(11,2))

    def __init__(self):
        super().setupDBBase(iStrategy, iStrategy.strat_id, self.strat_id);

    def add_table(self):
        self.create_table();

    def register(self, STRAT_ID,STRAT, MAJOR, MINOR, DESC):
        self.strat_id = STRAT_ID;
        self.strategy = STRAT;
        self.major_version = MAJOR;
        self.minor_version = MINOR;
        self.strat_desc = DESC;

        self.db_save();

    def set_weights(self):
        pass

    def get_combs(self):
        pass
        
    def run_session(self):
        pass

    def validate_tickets(self):
        pass
        



