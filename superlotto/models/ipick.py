'''
Created on Jan 21, 2018

@author: somaj
'''
class iPick:
    p=[0 for x in range(5)]
    
    def __init__(self, pick5=[0 for x in range(5)]):        
        
            self.setArray(pick5);
        
    def __getitem__(self, index):
        return self.p[index];
    
    def __setitem__(self, index, value):
        self.p[index] = value;
        
    def getArray(self):
        return self.p;
    
    def setArray(self, pick5=[]):
        self.p = pick5    
#         self.p1=pick20[0];
#         self.p2=pick20[1];
#         self.p3=pick20[2];
#         self.p4=pick20[3];
#         self.p5=pick20[4]
#         self.p6=pick20[5]
#         self.p7=pick20[6]
#         self.p8=pick20[7]
#         self.p9=pick20[8]
#         self.p10=pick20[9]
#         self.p11=pick20[10]
#         self.p12=pick20[11]
#         self.p13=pick20[12]
#         self.p14=pick20[13]
#         self.p15=pick20[14]
#         self.p16=pick20[15]
#         self.p17=pick20[16]
#         self.p18=pick20[17]
#         self.p19=pick20[18]
#         self.p20=pick20[19]
    
    def toString(self):
        return "["+" ".join(str(x) for x in self.getArray()) +"]"
