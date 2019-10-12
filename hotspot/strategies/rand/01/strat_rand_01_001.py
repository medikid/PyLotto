from hotspot.models.istrategy import iStrategy


class Strat_rand_01_001(iStrategy):
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
        print("Run from "+self.STRAT_ID)
        print("Pick "+str(no_picks)+" nums and get "+str(no_tickets)+" tickets for Draw_Id "+str(draw_id))