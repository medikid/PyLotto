from sqlalchemy import Column, Integer, Numeric, String, Text, VARCHAR, DECIMAL, DateTime, Float, Boolean, LargeBinary, Binary, SmallInteger, BigInteger
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from hotspot.db import db_init;
from hotspot.db.db_base import DBBase
from hotspot.models import Base, ipick, iresult, idraw, ibin

import numpy as np

class iPreds(Base, DBBase):
    __tablename__ = 'preds'
    db = db_init();

    sess_id=Column(BigInteger, primary_key=True, autoincrement=False)
    p1=Column(DECIMAL(6,4))
    p2=Column(DECIMAL(6,4))
    p3=Column(DECIMAL(6,4))
    p4=Column(DECIMAL(6,4))
    p5=Column(DECIMAL(6,4))
    p6=Column(DECIMAL(6,4))
    p7=Column(DECIMAL(6,4))
    p8=Column(DECIMAL(6,4))
    p9=Column(DECIMAL(6,4))
    p10=Column(DECIMAL(6,4))
    p11=Column(DECIMAL(6,4))
    p12=Column(DECIMAL(6,4))
    p13=Column(DECIMAL(6,4))
    p14=Column(DECIMAL(6,4))
    p15=Column(DECIMAL(6,4))
    p16=Column(DECIMAL(6,4))
    p17=Column(DECIMAL(6,4))
    p18=Column(DECIMAL(6,4))
    p19=Column(DECIMAL(6,4))
    p20=Column(DECIMAL(6,4))
    p21=Column(DECIMAL(6,4))
    p22=Column(DECIMAL(6,4))
    p23=Column(DECIMAL(6,4))
    p24=Column(DECIMAL(6,4))
    p25=Column(DECIMAL(6,4))
    p26=Column(DECIMAL(6,4))
    p27=Column(DECIMAL(6,4))
    p28=Column(DECIMAL(6,4))
    p29=Column(DECIMAL(6,4))
    p30=Column(DECIMAL(6,4))
    p31=Column(DECIMAL(6,4))
    p32=Column(DECIMAL(6,4))
    p33=Column(DECIMAL(6,4))
    p34=Column(DECIMAL(6,4))
    p35=Column(DECIMAL(6,4))
    p36=Column(DECIMAL(6,4))
    p37=Column(DECIMAL(6,4))
    p38=Column(DECIMAL(6,4))
    p39=Column(DECIMAL(6,4))
    p40=Column(DECIMAL(6,4))
    p41=Column(DECIMAL(6,4))
    p42=Column(DECIMAL(6,4))
    p43=Column(DECIMAL(6,4))
    p44=Column(DECIMAL(6,4))
    p45=Column(DECIMAL(6,4))
    p46=Column(DECIMAL(6,4))
    p47=Column(DECIMAL(6,4))
    p48=Column(DECIMAL(6,4))
    p49=Column(DECIMAL(6,4))
    p50=Column(DECIMAL(6,4))
    p51=Column(DECIMAL(6,4))
    p52=Column(DECIMAL(6,4))
    p53=Column(DECIMAL(6,4))
    p54=Column(DECIMAL(6,4))
    p55=Column(DECIMAL(6,4))
    p56=Column(DECIMAL(6,4))
    p57=Column(DECIMAL(6,4))
    p58=Column(DECIMAL(6,4))
    p59=Column(DECIMAL(6,4))
    p60=Column(DECIMAL(6,4))
    p61=Column(DECIMAL(6,4))
    p62=Column(DECIMAL(6,4))
    p63=Column(DECIMAL(6,4))
    p64=Column(DECIMAL(6,4))
    p65=Column(DECIMAL(6,4))
    p66=Column(DECIMAL(6,4))
    p67=Column(DECIMAL(6,4))
    p68=Column(DECIMAL(6,4))
    p69=Column(DECIMAL(6,4))
    p70=Column(DECIMAL(6,4))
    p71=Column(DECIMAL(6,4))
    p72=Column(DECIMAL(6,4))
    p73=Column(DECIMAL(6,4))
    p74=Column(DECIMAL(6,4))
    p75=Column(DECIMAL(6,4))
    p76=Column(DECIMAL(6,4))
    p77=Column(DECIMAL(6,4))
    p78=Column(DECIMAL(6,4))
    p79=Column(DECIMAL(6,4))
    p80=Column(DECIMAL(6,4))

    def __init__(self, sessID=0):
        self.sess_id=sessID
        self.reset()
        
        super().setupDBBase(iPreds, iPreds.sess_id, self.sess_id)

    def add_table(self):
        self.create_table()

    def reset(self):        
        for i in range(81):
            if i>0:
                setattr(self, "p"+str(i), 0.0000);

    def set_pred(self, pos, pred):
        setattr(self, "p"+str(pos), pred)

    def get_pred(self, pos):
        return getattr(self, "p"+str(pos));