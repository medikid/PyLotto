from hotspot.models.istrategy import iStrategy

from hotspot.strategies.rand import RAND


class Strat_rand_01_001(RAND):
    STRAT_ID = "RAND.01.001"
    STRAT="RAND"
    MAJOR = 1
    MINOR = 1
    DESC="Picks number randomly using numpy random module"

    def __init__(self):       
        super().__init__()
    
    def register(self):
        super().register(self.STRAT_ID, self.STRAT, self.MAJOR, self.MINOR, self.DESC)

    def run(self, draw_id, no_tickets, no_picks):
        pick_array = []
        print("From "+self.STRAT_ID);
        print("Pick "+str(no_picks)+" nums and get "+str(no_tickets)+" tickets for Draw_Id "+str(draw_id))
        
        i=0;
        while (i < no_tickets):
            pick_array.append(super().pickRand(list(range(1,80)), no_picks));
            i+=1;
        return pick_array;

    def pickRand(self, no_picks):
        return super().pickRand(no_picks)