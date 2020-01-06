from hotspot.models.iexplore import iExplore

import numpy as np
import importlib

class Explore():
    _EXPLORE = {}
    _LOGS = {}
    _LABEL = None


    def __init__(self, Label=None, DrawID=0, Cnt=10, isCurrent=False):
        if (Label != None):
            self._LABEL = Label
            self._EXPLORE = self.load_algo(Label, DrawID, Cnt, isCurrent)

    def load_algo(self, Label, DrawID, Cnt, isCurrent):
        mod = "hotspot.explore.algos."+ str(Label).lower();
        clas = str(Label).upper();

        md = importlib.import_module(mod)
        cl =  getattr(md, clas)
        self._EXPLORE = cl(DrawID, Cnt, isCurrent);

    def run(self):
        self._EXPLORE.explore();

