
from hotspot.models.iexplore import iExplore
from hotspot.models.index import Index


class DEPTH_0_4(iExplore):
    LABEL = 'DEPTH_0_4';
    DESC = 'Numbers win in the last 5 draws'

 
    def __init__(self, DrawID=0, Cnt=0, isCurrent=False):
        super(DEPTH_0_4, self).__init__(self.LABEL, DrawID, Cnt, isCurrent)

        #super().LABEL = self.LABEL
        #super().DESC = self.DESC;
        # self.LABEL = 'PREV_WINS';
        # self.DESC = 'Numbers with consecutive second wins i.e. with depth of 0-0'
        iExplore.LABEL = self.LABEL
        iExplore.DESC = self.DESC;

        #super()._INDEX = Index(self.LABEL, self.DESC)

        print("Index DEPTH_0_4 initiated");


    def execute_algo(self, X, Y):
        qualify = False;
        if (super()._DEPTHS[X][Y] <= 4 ): 
            qualify = True;

        return qualify;
