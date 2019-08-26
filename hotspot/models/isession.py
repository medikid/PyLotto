from sqlalchemy import Column, Integer, Numeric, String, VARCHAR, DECIMAL, DateTime, Float, Boolean, LargeBinary, Binary, SmallInteger, BigInteger
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from hotspot.db import db_init;
from hotspot.db.db_base import DBBase
from hotspot.models import Base, ipick, iresult, idraw, ibin

import numpy as np

class iPrize(Base, DBBase):
    __tablename__ = 'sessions'
    db = db_init();

    sess_id=Column(Integer, primary_key=True, autoincrement=False)
    strat_id=Column(VARCHAR(11))
    date_time=Column(DateTime)
    tickets_total=Column(Integer)
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
        return 0;

    def add_table(self):
        self.create_table();

    