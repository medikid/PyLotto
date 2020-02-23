
from hotspot.models.iexplore import iExplore
from hotspot.models.index import Index


class PREV_WINS(iExplore):
    LABEL = 'PREV_WINS';
    DESC = 'Numbers with consecutive second wins i.e. with depth of 0-0'

 
    def __init__(self, DrawID=0, Cnt=0, isCurrent=False):
        super(PREV_WINS, self).__init__(self.LABEL, DrawID, Cnt, isCurrent)

        #super().LABEL = self.LABEL
        #super().DESC = self.DESC;
        # self.LABEL = 'PREV_WINS';
        # self.DESC = 'Numbers with consecutive second wins i.e. with depth of 0-0'
        iExplore.LABEL = self.LABEL
        iExplore.DESC = self.DESC;

        #super()._INDEX = Index(self.LABEL, self.DESC)

        print("Index PREV_WINS initiated");


    def execute_algo(self, X, Y):
        qualify = False;
        if (super()._DEPTHS[X][Y] == 0 and super()._DEPTHS[X-1][Y]== 0): 
            qualify = True;

        return qualify;
