from hotspot.models.isession import iSession

import importlib

class Session(iSession):
    _LOTTO = None
    _STRAT = None

    def __init__(self, lotto_name):
        self._LOTTO = lotto_name

        super().__init__()
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
        

    def run(self, strat_name, draw_id, no_tickets=1, no_picks=10):
        self.load_strategy(strat_name)      
        self._STRAT.run(draw_id, no_tickets, no_picks)

        #Run Strategy
        #Set Weights
        #pick nums /best or worst or random
        #repeat cycle to get no_ticks
        #save tickets
        #validate if results available
        #update metrics
        #print summary

        pass;