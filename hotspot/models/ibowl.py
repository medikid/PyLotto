from hotspot.models import iball

from numpy.random import choice as np_choice
import random as r




class iBowl:
    _size=0;
    _balls={}
    _scoretypes=[]

    def __init__(self, size):
        self._size = size;
        self.setup();
             

    def setup(self):
        i = 1; self._balls = {};
        while (i <= self._size):
            self._balls[i] = iball.iBall(i);
            i += 1;
    
    def initScoretype(self, score_type):        
        self._scoretypes.append(score_type);
        i = 1;
        while (i <= self._size):
            self._balls[i].setScore(score_type, 0.00);
            i += 1;

        


    def setScore(self, num, score_type, score):
        if (self._scoretypes.count(score_type) ==  0):
            self.initScoretype(score_type);
        
        self._balls[num].setScore(score_type, score)

    def getArrayNums(self):
        return list(self._balls);

    def getArrayScores(self, score_type):
        i = 1; arScores = [];
        while (i <= self._size):
            arScores.append(self._balls[i].getScore(score_type));
            i += 1;
        return arScores;

    def keyFromItem(self, func):
        return lambda item: func(*item)


    def sortedNumArray(self, score_type, second_score_type = None, asc = True):
        dictToSort = self._balls;
        sortedDict = {}
        #return sorted(self._balls.items(), key= self.keyFromItem( lambda k,v: (v.getScore(score_type), k)), reverse = asc)
        
        if ( second_score_type != None):
            sortedDict = sorted(dictToSort.items(), key= self.keyFromItem( lambda k, v: (v.getScore(score_type), v.getScore(second_score_type))), reverse = asc)
        else: sortedDict = sorted(dictToSort.items(), key= self.keyFromItem( lambda k, v: v.getScore(score_type)), reverse = asc)

        keys = [x[0] for x in sortedDict]; #convert tuple(k,v) to list if keys
        return keys;

    def pickRand(self, pick_n, np=False):
        sampleArray = self.getArrayNums();        
        picks = [];

        if (np==True):
            picks = np_choice(sampleArray, pick_n)
        else: picks = r.choices(sampleArray, k=pick_n)
        picks.sort();

        return picks;

    def pickWeightedRand(self,  pick_n, score_type="overall", np=False):
        sampleArray = self.getArrayNums();   
        weightsArray = self.getArrayScores(score_type)
        picks = [];

        if (np==True):
            picks = np_choice(sampleArray, pick_n, weightsArray)
        else: picks = r.choices(sampleArray, weightsArray, k=pick_n,  replace=False)
        picks.sort();
        
        return picks;


    def toString(self):
        i=1; str = "["
        while (i <= self._size):
            str += self._balls[i].toString()
            str += "\n"
            i += 1;
        str += "]"
        return str;


