from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean, LargeBinary, Binary, SmallInteger, BigInteger, VARCHAR
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from hotspot.db import db_init;
from hotspot.db.db_base import DBBase
from hotspot.models import Base, ipick, iresult, idraw, ibin, iprize

import numpy as np

class iTicket(Base, DBBase):
    __tablename__ = 'tickets'
    db = db_init();
    
    tick_id=Column(Integer,primary_key=True, autoincrement=True)    
    draw_id=Column(Integer)
    picks_total=Column(Integer)
    opt_x=Column(Boolean)
    strat_id=Column(VARCHAR(11))
    sess_id=Column(BigInteger)
    t1=Column(SmallInteger)
    t2=Column(SmallInteger)
    t3=Column(SmallInteger)
    t4=Column(SmallInteger)
    t5=Column(SmallInteger)
    t6=Column(SmallInteger)
    t7=Column(SmallInteger)
    t8=Column(SmallInteger)
    t9=Column(SmallInteger)
    t10=Column(SmallInteger)
    t11=Column(SmallInteger)
    t12=Column(SmallInteger)
    t13=Column(SmallInteger)
    t14=Column(SmallInteger)
    t15=Column(SmallInteger)
    t16=Column(SmallInteger)
    t17=Column(SmallInteger)
    t18=Column(SmallInteger)
    t19=Column(SmallInteger)
    t20=Column(SmallInteger)
    t21=Column(SmallInteger)
    t22=Column(SmallInteger)
    t23=Column(SmallInteger)
    t24=Column(SmallInteger)
    t25=Column(SmallInteger)
    t26=Column(SmallInteger)
    t27=Column(SmallInteger)
    t28=Column(SmallInteger)
    t29=Column(SmallInteger)
    t30=Column(SmallInteger)
    t31=Column(SmallInteger)
    t32=Column(SmallInteger)
    t33=Column(SmallInteger)
    t34=Column(SmallInteger)
    t35=Column(SmallInteger)
    t36=Column(SmallInteger)
    t37=Column(SmallInteger)
    t38=Column(SmallInteger)
    t39=Column(SmallInteger)
    t40=Column(SmallInteger)
    t41=Column(SmallInteger)
    t42=Column(SmallInteger)
    t43=Column(SmallInteger)
    t44=Column(SmallInteger)
    t45=Column(SmallInteger)
    t46=Column(SmallInteger)
    t47=Column(SmallInteger)
    t48=Column(SmallInteger)
    t49=Column(SmallInteger)
    t50=Column(SmallInteger)
    t51=Column(SmallInteger)
    t52=Column(SmallInteger)
    t53=Column(SmallInteger)
    t54=Column(SmallInteger)
    t55=Column(SmallInteger)
    t56=Column(SmallInteger)
    t57=Column(SmallInteger)
    t58=Column(SmallInteger)
    t59=Column(SmallInteger)
    t60=Column(SmallInteger)
    t61=Column(SmallInteger)
    t62=Column(SmallInteger)
    t63=Column(SmallInteger)
    t64=Column(SmallInteger)
    t65=Column(SmallInteger)
    t66=Column(SmallInteger)
    t67=Column(SmallInteger)
    t68=Column(SmallInteger)
    t69=Column(SmallInteger)
    t70=Column(SmallInteger)
    t71=Column(SmallInteger)
    t72=Column(SmallInteger)
    t73=Column(SmallInteger)
    t74=Column(SmallInteger)
    t75=Column(SmallInteger)
    t76=Column(SmallInteger)
    t77=Column(SmallInteger)
    t78=Column(SmallInteger)
    t79=Column(SmallInteger)
    t80=Column(SmallInteger)    
    tx=Column(Integer)
    t_bin0140=Column(BigInteger)
    t_bin4180=Column(BigInteger)
    t_matches=Column(Integer)
    tx_match=Column(Boolean)
    t_prize=Column(Float(2, True))
    
    tickDict=dict([(i,0) for i in range(1, 81) ])
    
    def __init__(self, tickID=0, drawID=0):
        self.reset()
        self.tick_id=tickID;
        self.draw_id=drawID;
        if (self.tick_id>0): self.setup()
        
        super().setupDBBase(iTicket, iTicket.tick_id, self.tick_id)
    
    def add_table(self):
        self.create_table();

    def reset(self):
        self.draw_id = 0;
        self.opt_x=0;
        self.picks_total = 0;
        self.tx = 0;
        self.t_bin0140 = 0;
        self.t_bin4180 = 0;
        self.t_matches = 0;
        self.tx_match = 0;
        self.t_prize = 0;
        for i in range(81):            
            self.tickDict[i]=0;
            if i>0:
                setattr(self, "t"+str(i), 0);
        self.tx = 0;
                
    def derive_bin(self):
        return 0;

    def setStratID(self, stratID):
        self.strat_id = stratID;

    def getStratID(self):
        return self.strat_id;

    def setSessionID(self, sessID):
        self.sess_id = sessID;

    def getSessionID(self):
        return self.sess_id;
        
    def setup(self):
        d = self.db.session.query(iTicket).filter(iTicket.tick_id==self.tick_id).first();
        if d is not None:
            self.picks_total=d.picks_total;
            self.opt_x=d.opt_x
            self.strat_id=d.strat_id
            self.sess_id=d.sess_id
            for i in self.tickDict.keys():
                if (i>0):
                    setattr(self, "t"+str(i), getattr(d,"t"+str(i)) )
                    #self.drawDict[i]=getattr(self, "t"+str(i))
            self.tx=d.tx
            self.t_bin0140=d.t_bin0140
            self.t_bin4180=d.t_bin4180
            self.t_matches=d.t_matches
            self.tx_match=d.tx_match
            self.t_prize=d.t_prize
    

    def toString(self):
        return str(self.get_dict())  + "[" + str(self.tx)+"]"
            
            
    def get_dict(self):
        dict={};
        dict[self.tick_id]=np.array([self.t1, self.t2, self.t3, self.t4, self.t5, self.t6, self.t7, self.t8, self.t9, self.t10, self.t11, self.t12, self.t13, self.t14, self.t15, self.t16, self.t17, self.t18, self.t19, self.t20, self.t21, self.t22, self.t23, self.t24, self.t25, self.t26, self.t27, self.t28, self.t29, self.t30, self.t31, self.t32, self.t33, self.t34, self.t35, self.t36, self.t37, self.t38, self.t39, self.t40, self.t41, self.t42, self.t43, self.t44, self.t45, self.t46, self.t47, self.t48, self.t49, self.t50, self.t51, self.t52, self.t53, self.t54, self.t55, self.t56, self.t57, self.t58, self.t59, self.t60, self.t61, self.t62, self.t63, self.t64, self.t65, self.t66, self.t67, self.t68, self.t69, self.t70, self.t71, self.t72, self.t73, self.t74, self.t75, self.t76, self.t77, self.t78, self.t79, self.t80]);
        return dict;

    def get_picks_size(self):
        return self.picks_total;

    def derive_prize(self):
        pr = iprize.iPrize(self.picks_total, self.t_matches);
        if (self.tx == 1):
            self.t_prize = pr.prize_x;
        else: self.t_prize = pr.prize;
        

    def validate(self, drawID, d_bin0140, d_bin4180):
        t_matches=0;
        if (self.draw_id ==  drawID):      
            t_match_0140 = d_bin0140 & self.t_bin0140
            t_match_4180 = d_bin4180 & self.t_bin4180
            print("Draw 1-40:   ", '{0:040b}'.format(d_bin0140))
            print("Ticket 1-40: ", '{0:040b}'.format(self.t_bin0140))
            print("Match 1-40:  ", '{0:040b}'.format(t_match_0140))
            print("             ")
            print("Draw 41-80:   ", '{0:040b}'.format(d_bin0140))
            print("Ticket 41-80: ", '{0:040b}'.format(self.t_bin4180))
            print("Match 41-80:  ", '{0:040b}'.format(t_match_4180))

            t_matches += bin(t_match_0140).count("1")
            t_matches += bin(t_match_4180).count("1")
        self.t_matches = t_matches;

        self.derive_prize();

        #update db
        #self.db_update({'t_matches':self.t_matches, 'tx_match': self.tx_match, 't_prize':self.t_prize},{'tick_id': self.tick_id})
        #self.db_update({iTicket.t_matches:self.t_matches, iTicket.tx_match: self.tx_match, iTicket.t_prize:self.t_prize},{iTicket.tick_id: self.tick_id})
        
        query = self.db.session.query(iTicket).filter(iTicket.tick_id == self.tick_id).update({iTicket.t_matches:self.t_matches, iTicket.tx_match: self.tx_match, iTicket.t_prize:self.t_prize}, synchronize_session='fetch');
        self.db.session.commit()



    def fill_ticket(self, drawID, pick_array, pick_x=0):
        print("Filling ticket for", pick_array)
        self.draw_id = drawID
        b0140 = ibin.iBin();
        b4180 = ibin.iBin();
        bx = ibin.iBin();

        self.picks_total = len(pick_array)
        if (pick_x > 0):
            self.opt_x = 1;
            self.tx = pick_x

        for p in pick_array:
            setattr(self, "t"+str(p), 1);
            if p > 40:
                posn = p - 40;
                b4180.set_bit(posn);
            else: b0140.set_bit(p)
        
        #self.t_bin0140 = bytes('{0:040b}'.format(b0140.get_bin()), 'utf-8');
        #self.t_bin4180 = bytes('{0:040b}'.format(b4180.get_bin()), 'utf-8');

        #self.t_bin0140 = '{0:040b}'.format(b0140.get_bin());
        #self.t_bin4180 = '{0:040b}'.format(b4180.get_bin());

        # self.t_bin0140 = b0140.get_bin().to_bytes(40, byteorder='big');
        # self.t_bin4180 = b4180.get_bin().to_bytes(40, byteorder='big');

        #self.t_bin0140 = b0140.to_string();
        #self.t_bin4180 = b4180.to_string();

        self.t_bin0140 = b0140.get_bin(); #770947678208
        self.t_bin4180 = b4180.get_bin();  #8606711840

        # self.t_bin0140 = bin(b0140.get_bin()); #0b1011001110000000000100000000000000000000 
        # self.t_bin4180 = bin(b4180.get_bin()); #0b1000000001000000000000000000100000


    def print_bins(self):
        print('{0:040b}'.format(self.t_bin0140))
        print('{0:040b}'.format(self.t_bin4180))

    def print_ticket(self):
        print(str(self.draw_id),":[",self.get_dict(),"]")
        print('{0:040b}'.format(self.t_bin0140),'{0:040b}'.format(self.t_bin4180))

    def print_ticket_result(self):
        print(str(self.draw_id),":[",self.get_dict(),"]")
        print('{0:040b}'.format(self.t_bin0140),'{0:040b}'.format(self.t_bin4180))
                
        print("pick size: ", len(pick_array));
        print(self.toString())
