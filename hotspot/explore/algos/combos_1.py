
from hotspot.models.iexplore import iExplore
from hotspot.models.index import Index


class COMBOS_1(iExplore):
    LABEL = 'COMBOS_1';
    DESC = 'Combos of indices'

    ##[x,x,x,x,x,x]
    ##[0,x,0,x,0,x]
    ##[1,0,0,0,1,x]

 
    def __init__(self, DrawID=0, Cnt=0, isCurrent=False):
        super(COMBOS_1, self).__init__(self.LABEL, DrawID, Cnt, isCurrent)

        #super().LABEL = self.LABEL
        #super().DESC = self.DESC;
        # self.LABEL = 'PREV_WINS';
        # self.DESC = 'Numbers with consecutive second wins i.e. with depth of 0-0'
        iExplore.LABEL = self.LABEL
        iExplore.DESC = self.DESC;

        #super()._INDEX = Index(self.LABEL, self.DESC)

        print("Index COMBOS_1 initiated");


    def execute_algo(self, X, Y):
        qualify = False;
        if (super()._DEPTHS[X][Y] == 0 and super()._DEPTHS[X-1][Y]== 0):
            if (Y < 79 and super()._DEPTHS[X][Y+1] == 0 and super()._DEPTHS[X][Y+2]== 1):
                qualify = True;
            elif (Y > 2 and super()._DEPTHS[X][Y-1] == 0 and super()._DEPTHS[X][Y-2]== 1):
                qualify = True;

        return qualify;
