
from hotspot.models.istrategy import iStrategy

from numpy.random import choice as np_choice
from random import choices as r_choices

class RAND(iStrategy):

    def __init__(self):
        super().__init__();
    
    def pickRand(self, sampleArray, pick_n, np=False):
        picks = [];

        if (np==True):
            picks = np_choice(sampleArray, pick_n)
        else: picks = r_choices(sampleArray, k=pick_n)

        return picks;

    def pickWeightedRand(self, sampleArray, weightsArray, pick_n, np=False):
        picks = [];

        if (np==True):
            picks = np_choice(sampleArray, pick_n, weightsArray)
        else: picks = r_choices(sampleArray, weightsArray, k=pick_n)

        return picks;

