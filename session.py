from hotspot.models.isession import iSession
from hotspot.models.iticket import iTicket
from hotspot.models.idraw import iDraw

import importlib

class Session(iSession):
    _LOTTO = None
    _STRAT = None
    _CURRENT_SESSION=None
    _TICKETS = {}

    def __init__(self, lotto_name):
        self._LOTTO = lotto_name

        self._CURRENT_SESSION = super().__init__()
        pass;

    def load_strategy(self, strat_name):
        segs = strat_name.split("_");
        mod = self._LOTTO+".strategies"
        clas = "Strat_"+strat_name

        strat_name = segs[0]
        major_v=segs[1]
        minor_v=segs[2]

        if strat_name == "ai":
            mod += ".ai"
            if major_v == "01":
                mod += ".tf"
            elif major_v=="02":
                mod += ".pytorch"
        elif strat_name == "rand":
            mod += ".rand"
            mod += "."+major_v

        md = importlib.import_module(mod)
        cl =  getattr(md, clas)
        self._STRAT = cl();
            
        
        print("Module: ", mod)
        print("Class:", clas)
    
    def save(self):
        self.db_save();

    def run(self, stratName, drawID, no_tickets=1, no_picks=10, validate=False):
        #load strategy
        self.load_strategy(stratName)           

        #generate Session ID
        self.sess_id = super().generateSessionID()

        #setup session and initial save
        self.strat_id = self._STRAT.STRAT_ID;
        self.tickets_total = no_tickets;
        self.save();

        #Run Strategy to get picks array
        pick_array = self._STRAT.run(drawID, no_tickets, no_picks)
        print("PICK ARRAY", pick_array)
        #fill tickets from pick nums
       
        for picks in pick_array:
            tick = iTicket(0, drawID);
            tick.setStratID(self.strat_id);
            tick.setSessionID(self.sess_id)
            print("Picks", picks)
            tick.fill_ticket(drawID, picks);
            tick.db_save();

        #validate if results available
        if (validate==True):
            self.validateTickets(drawID)
        
        #update metrics
        self.updateSessionMetrics();

        #print summary
        self.printSummary()

        pass;

    def validateTickets(self, drawID):
        #pull all tickets
        ticks = super().get_tickets_all();
        
        #pull draw_id bin
        dr = iDraw(drawID);
        dr.setup();

        #validate and save results
        for tick in ticks:
            tick.validate(drawID, dr.d_bin0140, dr.d_bin4180)

