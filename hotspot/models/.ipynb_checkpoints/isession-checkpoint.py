from sqlalchemy import Column, Integer, Numeric, String, VARCHAR, DECIMAL, DateTime, Float, Boolean, LargeBinary, Binary, SmallInteger, BigInteger
from sqlalchemy import select, delete, update, insert
from sqlalchemy import func, distinct, ForeignKey
#from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from hotspot.db import db_init;
from hotspot.db.db_base import DBBase
from hotspot.models import Base, ipick, iresult, idraw, ibin, iticket

import numpy as np
from datetime import datetime

class iSession(Base, DBBase):
    __tablename__ = 'sessions'
    db = db_init();

    sess_id=Column(BigInteger, primary_key=True, autoincrement=False)
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

    picks = 0;

    #sessions = relationship('draws',)

    def __init__(self, sessionID=0):
        self.reset();
        self.generateSessionID();
        if(sessionID>0):
            self.sess_id = sessionID;

        super().setupDBBase(iSession, iSession.sess_id, self.sess_id)

    def reset(self):
        self.sess_id=0
        self.strat_id=0
        self.date_time= datetime.now()
        self.tickets_total=0
        self.tickets_claimed=0
        self.cost_total=0
        self.prize_total=0
        self.pnl=0
        self.match_max=0
        self.prize_max=0
        self.match_min=0
        self.prize_min=0
        self.match_average=0
        self.prize_average=0

        self.picks = 0;

    

    def add_table(self):
        self.create_table();

    def generateSessionID(self):
        sess_id_format = "%Y%m%d%H%M%S"
        self.date_time = datetime.now();
        
        self.set_session_id(self.date_time.strftime(sess_id_format))
        print("New Session ID: ", self.sess_id)
        return self.sess_id;

    def save(self):
        self.db_save();


    def get_session_id(self):
        return self.sess_id;
    
    def set_session_id(self, sessID):
        self.sess_id = sessID;

    def get_tickets_all(self):   
        ticks = self.db.session.query(iticket.iTicket).filter(iticket.iTicket.sess_id==self.sess_id).all();
        #ticks = self.db.session.commit();
        self.picks = ticks[0].picks_total
        return ticks

    def updateSessionMetrics(self):
        self.match_max = self.db.session.query(func.max(iticket.iTicket.t_matches)).filter(iticket.iTicket.sess_id==self.sess_id).scalar();
        self.prize_total = self.db.session.query(func.sum(iticket.iTicket.t_prize)).filter(iticket.iTicket.sess_id==self.sess_id).scalar();
        
        self.cost_total = self.tickets_total * 1.00;
        self.tickets_claimed = self.db.session.query(func.count(iticket.iTicket.t_prize)).filter(iticket.iTicket.sess_id==self.sess_id).filter(iticket.iTicket.t_prize > 0).scalar();
        
        #iSession.update().where(iSession.sess_id == self.sess_id).values(iSession.match_max=self.match_max, iSession.prize_total = self.prize_total, iSession.cost_total=self.cost_total, iSession.prize_total = self.prize_total)
        
        self.db.session.query(iSession).filter(iSession.sess_id == self.sess_id).update({iSession.match_max:self.match_max, iSession.prize_total : self.prize_total, iSession.cost_total: self.cost_total, iSession.prize_total : self.prize_total}, synchronize_session='fetch');
        


    def printSummary(self):
        print("Strategy: ", self.strat_id,  "Session ID: ", self.sess_id)        
        print("Total Tickets: ", self.tickets_total, "Picks/Tickets: ")
        print("Max Match: ", self.match_max, "Tickets Claimed: ", self.tickets_claimed)
        print("Total Cost: ", self.cost_total, "Total Prize: ", self.prize_total)
    