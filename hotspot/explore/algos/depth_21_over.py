
from hotspot.models.iexplore import iExplore
from hotspot.models.index import Index


class DEPTH_21_OVER(iExplore):
    LABEL = 'DEPTH_21_OVER';
    DESC = 'Depths over 21'

 
    def __init__(self, DrawID=0, Cnt=0, isCurrent=False):
        super(DEPTH_21_OVER, self).__init__(self.LABEL, DrawID, Cnt, isCurrent)

        #super().LABEL = self.LABEL
        #super().DESC = self.DESC;
        # self.LABEL = 'PREV_WINS';
        # self.DESC = 'Numbers with consecutive second wins i.e. with depth of 0-0'
        iExplore.LABEL = self.LABEL
        iExplore.DESC = self.DESC;

        #super()._INDEX = Index(self.LABEL, self.DESC)

        print("Index DEPTH_21_over initiated");


    def execute_algo(self, X, Y):
        qualify = False;
        if (super()._DEPTHS[X][Y] >= 21): 
            qualify = True;

        return qualify;
