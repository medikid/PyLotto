
from hotspot.models.iexplore import iExplore


class PREV_WINS(iExplore):
    LABEL = 'PREV_WINS';
    DESC = 'Numbers with consecutive second wins i.e. with depth of 0-0'

 
    def __init__(self,  DrawID=0, Cnt=0, isCurrent=False):
        super().__init__(self.LABEL, DrawID, Cnt, isCurrent)

        print("Index PREV_WINS initiated")
        pass;

    def execute_algo(self, X, Y):
        qualify = False;
        if (super()._DRAWS[X][Y] == 1 and super()._DRAWS[X-1][Y]== 1): 
            qualify = True;

        return qualify;
