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
    __tablename__ = 'prizes'
    db = db_init();
    
    prz_id=Column(VARCHAR(20),primary_key=True, autoincrement=False)
    lottery=Column(VARCHAR(20))
    country=Column(VARCHAR(20))
    state=Column(VARCHAR(20))
    picks=Column(Integer)
    matches=Column(Integer)
    cost=Column(DECIMAL(5,2))
    prize=Column(DECIMAL(11,2))
    cost_x=Column(DECIMAL(5, 2))
    prize_x=Column(DECIMAL(11, 2))
    odds=Column(DECIMAL(5, 2))
    odds_x=Column(DECIMAL(5,2))

    tickDict={0:0}
    
    def __init__(self):
        #CONSTANTS#
        self.lottery = "Hotspot"
        self.country = "USA";
        self.state = "CA"

    def add_table(self):
        self.create_table();
        

    def get_prize(self, picks, matches):
        p = 0;

        return p;