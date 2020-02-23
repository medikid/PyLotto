
from hotspot.models.iexplore import iExplore
from hotspot.models.index import Index


class DIAG_4_WINS(iExplore):
    LABEL = 'DIAG_4_WINS';
    DESC = 'Numbers with diagonal wins four times i.e. with depth of X-0-1-2-3'

 
    def __init__(self, DrawID=0, Cnt=0, isCurrent=False):
        super(DIAG_4_WINS, self).__init__(self.LABEL, DrawID, Cnt, isCurrent)

        #super().LABEL = self.LABEL
        #super().DESC = self.DESC;
        # self.LABEL = 'PREV_WINS';
        # self.DESC = 'Numbers with consecutive second wins i.e. with depth of 0-0'
        iExplore.LABEL = self.LABEL
        iExplore.DESC = self.DESC;

        #super()._INDEX = Index(self.LABEL, self.DESC)

        print("Index DIAG_4_WINS initiated");


    def execute_algo(self, X, Y):
        qualify = False;
        if (Y < 77 and super()._DEPTHS[X][Y+1] == 0 and super()._DEPTHS[X][Y+2]== 1 and super()._DEPTHS[X][Y+3] == 2 and super()._DEPTHS[X][Y+4]==3 ): 
            qualify = True;
        if (Y > 4 and super()._DEPTHS[X][Y-1] == 0 and super()._DEPTHS[X][Y-2]== 1 and super()._DEPTHS[X][Y-3] == 2 and super()._DEPTHS[X][Y-4] == 3): 
            qualify = True;
            

        return qualify;
