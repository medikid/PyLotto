


class iBall:
    _num=0
    _scores={}

    def __init__(self, num):
        self.reset();
        self.setNum(num);

    def reset(self):
        self._num = 0;
        self._scores={}

    def setNum(self, num):
        self._num =  num;
    
    def getNum(self):
        return self._num;
    
    def setScore(self, score_type, score):
        self._scores[score_type] = score;

    def getScore(self, score_type):
        return self._scores[score_type];

    def toString(self):
        return str(self._num) + "[" + str(self._scores) + "]";