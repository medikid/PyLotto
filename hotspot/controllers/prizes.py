from hotspot.models import iprize

from hotspot.db import db_init;
from hotspot.db.db_base import DBBase

import numpy as np


class Prizes(iprize.iPrize):
    db = db_init();
    r_prizes = {};

    def __init__(self):
        self.lotto = "Hotspot";
        self.r_prizes = {};

    def setup_prize_list(self):
        results = self.db.session.query(iprize.iPrize).filter(iprize.iPrize.lottery==self.lotto).all()

        for result in results:
            self.r_prizes[result.prz_id] = result;            
        
    
    def get_prize(self, picks, matches):
        przID = "Hotspot"+"_"+str(picks)+"_"+str(matches);
        return self.r_prizes[przID];
