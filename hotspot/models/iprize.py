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
    
    def __init__(self, picks=0, matches=0):
        #CONSTANTS#
        self.lottery = "Hotspot"
        self.country = "USA";
        self.state = "CA"   

        #load
        if(picks > 0):
            self.setup(picks, matches);


    def add_table(self):
        self.create_table();

    def derive_prize_id(self, picks, matches):
        self.picks = picks;
        self.matches = matches;
        self.prz_id = self.lottery + "_" + str(self.picks) + "_" + str(self.matches)
        print("PRIZE ID: ", self.prz_id)

    def setup(self, picks, matches):
        self.derive_prize_id(picks, matches);
        prz = self.db.session.query(iPrize).filter(iPrize.prz_id==self.prz_id).first();

        self.lottery=prz.lottery
        self.country=prz.country
        self.state=prz.state
        self.picks=prz.picks
        self.matches=prz.matches
        self.cost=prz.cost
        self.prize=prz.prize
        self.cost_x=prz.cost_x
        self.prize_x=prz.prize_x
        self.odds=prz.odds
        self.odds_x=prz.odds_x

    def to_string(self):
        return self.prz_id

    