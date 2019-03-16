import random
from SuperLotto.super_lotto import SuperLotto

class NumPick(object):
    draws = [];
    pick_balls = [];
    mega_balls = [];
    nums = [];
    probs = [];
    
#     pops = list(range(0,21));
# probs = [0,0,1,0,2,0,3,0,4,0,5,0,5,0,4,0,3,0,2,0];
# #probs = sorted(list(range(0,47)), reverse=True);
# picks = []
# n=3
#     
# def pickNums(self,Pops,Probs,N):
#     picks = random.choices(Pops, Probs, k=N);
#     print(picks)
#  
# picks = random.choices(pops, probs, k=3)
# print(picks);
    
    def __init__(self, super_lotto):
        self.sl = super_lotto;
        self.draws = self.sl.get_draws_array();
        self.setup();        
        
    
    def setup(self):
        initial_value = 0;
        for i in range(48):
            self.pick_balls.append(initial_value);
        print(self.pick_balls);
        
        for j in range(28):
            self.mega_balls.append(initial_value);
        
    def reset(self, init_val):
        for i in range(48):
            self.pick_balls.append(init_val);
        print(self.pick_balls);
        
        for j in range(28):
            self.mega_balls.append(init_val);
        
    def calc_freq(self, num_draws):
        self.reset(0);
        for i in range(0,num_draws):
            draw = self.draws[i];
            draw.print_draw()
            self.pick_balls[draw.num_1] += 1;
            self.pick_balls[draw.num_2] += 1;
            self.pick_balls[draw.num_3] += 1;
            self.pick_balls[draw.num_4] += 1;
            self.pick_balls[draw.num_5] += 1;
            self.mega_balls[draw.mega] += 1;
            
    def print_freq(self):       
        for i in range(48):
            print('{0}->[{1}] \n'.format(i,self.pick_balls[i]));
        
    
    def calc_probs(self, num_draws, v=1):
        self.reset(5);
        self.num_picks[0]=0;
        if (v == 1):
            self.calc_probs_v1(num_draws);
                
    def calc_probs_v1(self, num_draws):
        for i in range(num_draws):
            if i == 0:
                self.set_prob_0(self.draws[i]);
                print("if Probs in 0 {0}".format([i]))
            elif i in range(1,3):
                self.set_prob_1(self.draws[i]);
                print("elif probs in 1,2 {0}".format([i]))
            elif i in range(3,20):
                self.set_prob_3(self.draws[i])
                print("elif propbs in 3->7 {0}".format([i]))
                
        
    
    def set_prob_0(self, draw):
        self.pick_balls[draw.num_1] = 0;
        self.pick_balls[draw.num_2] = 0;
        self.pick_balls[draw.num_3] = 0;
        self.pick_balls[draw.num_4] = 0;
        self.pick_balls[draw.num_5] = 0;
        self.mega_balls[draw.mega] = 0;
    
    def set_prob_1(self, draw):
        self.pick_balls[draw.num_1] = 1;
        self.pick_balls[draw.num_2] = 1;
        self.pick_balls[draw.num_3] = 1;
        self.pick_balls[draw.num_4] = 1;
        self.pick_balls[draw.num_5] = 1;
        self.mega_balls[draw.mega] = 0;
        
    def set_prob_2(self, draw):
        self.pick_balls[draw.num_1] = 2;
        self.pick_balls[draw.num_2] = 2;
        self.pick_balls[draw.num_3] = 2;
        self.pick_balls[draw.num_4] = 2;
        self.pick_balls[draw.num_5] = 2;
        self.mega_balls[draw.mega] = 0;
    
    def set_prob_3(self, draw):
        self.pick_balls[draw.num_1] = 3;
        self.pick_balls[draw.num_2] = 3;
        self.pick_balls[draw.num_3] = 3;
        self.pick_balls[draw.num_4] = 3;
        self.pick_balls[draw.num_5] = 3;
        self.mega_balls[draw.mega] = 0;
    
    def set_prob_4(self, draw):
        self.pick_balls[draw.num_1] = 4;
        self.pick_balls[draw.num_2] = 4;
        self.pick_balls[draw.num_3] = 4;
        self.pick_balls[draw.num_4] = 4;
        self.pick_balls[draw.num_5] = 4;
        self.mega_balls[draw.mega] = 0;
    
    def set_prob_5(self, draw):
        self.pick_balls[draw.num_1] = 5;
        self.pick_balls[draw.num_2] = 5;
        self.pick_balls[draw.num_3] = 5;
        self.pick_balls[draw.num_4] = 5;
        self.pick_balls[draw.num_5] = 5;
        self.mega_balls[draw.mega] = 0;       
        