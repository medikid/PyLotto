import csv
from SuperLotto.super_lotto import SuperLotto
    
class PickDepth(object):
            pickdepth_file_csv = "E:/Projects/Lotto/superlotto/Results/PickDepth.csv"
            draw_file_csv = "E:/Projects/Lotto/superlotto/Results/Draws.csv"
            depths = [];
         
            def write_pick_depth_csv(self):
                out = csv.writer(open(self.pickdepth_file_csv,"w", newline=''), delimiter=',',quoting=csv.QUOTE_NONE)
                out.writerow(["draw_id", "date", "day", "num_1", "num_2", "num_3", "num_4", "num_5", "mega"]);
                for x in range(len(self.draws)):
                    draw_id = self.draws[x].draw_id;
                    pd = self.get_pick_depth(draw_id);
                    out.writerow(pd.get_pd1_array());
                
            def read_pick_depth_csv(self): 
                rows = csv.reader(open(self.pickdepth_file_csv,'rt'));
                for row in rows:
                    print(row);
                      
            
            def get_pick_depth(self, drawID):
                n = 0;
                depth_count = 0;
                d = self.Depth(drawID);
                               
                for i in range(len(self.draws)):
                    if(self.draws[i].draw_id == drawID):
                        n = i;
                        depth_count = 12;
                        d.date = self.draws[n].get_date();
                        self.draws[n].print_draw();
                    
                    if (n > 0 and depth_count > 0 and i > n):
                        draw_set = {self.draws[i].num_1,self.draws[i].num_2,self.draws[i].num_3,self.draws[i].num_4,self.draws[i].num_5};
                        
                        if(self.draws[n].num_1 in draw_set):
                            if (d.num_1_depth_1 == 0):
                                d.num_1_depth_1 = i - n;
                                depth_count -= 1;
                            elif (d.num_1_depth_2 == 0):
                                d.num_1_depth_2 = i - n;
                                depth_count -= 1;
                                
                        if(self.draws[n].num_2 in draw_set):  
                            if (d.num_2_depth_1 == 0):
                                d.num_2_depth_1 = i - n;
                                depth_count -= 1;
                            elif (d.num_2_depth_2 == 0):
                                d.num_2_depth_2 = i - n;
                                depth_count -= 1;
                        
                        if(self.draws[n].num_3 in draw_set): 
                            if (d.num_3_depth_1 == 0):
                                d.num_3_depth_1 = i - n;
                                depth_count -= 1;
                            elif (d.num_3_depth_2 == 0):
                                d.num_3_depth_2 = i - n;
                                depth_count -= 1;
                                
                        if(self.draws[n].num_4 in draw_set): 
                            if (d.num_4_depth_1 == 0):
                                d.num_4_depth_1 = i - n;
                                depth_count -= 1;
                            elif (d.num_4_depth_2 == 0):
                                d.num_4_depth_2 = i - n;
                                depth_count -= 1; 
                        
                        if(self.draws[n].num_5 in draw_set):
                            if (d.num_5_depth_1 == 0):
                                d.num_5_depth_1 = i - n;
                                depth_count -=1;
                            elif (d.num_5_depth_2 == 0):
                                d.num_5_depth_2 = i - n;
                                depth_count -= 1;
                        
                        if(self.draws[n].mega == self.draws[i].mega):
                            if (d.mega_depth_1 == 0):
                                d.mega_depth_1 = i - n;
                                depth_count -= 1;
                            elif (d.mega_depth_2 == 0):
                                d.mega_depth_2 = i - n;
                                depth_count -= 1;
                        
                d.printDepth();
                return d;
                
            def __init__(self, super_lotto):
                self.sl = super_lotto;
                self.draws = self.sl.get_draws_array();
                
                
                
            class Depth(object):
                draw_id = 0;
                date = '';
                num_1_depth_1 = 0;
                num_1_depth_2 = 0;
                num_2_depth_1 = 0;
                num_2_depth_2 = 0;
                num_3_depth_1 = 0;
                num_3_depth_2 = 0;
                num_4_depth_1 = 0;
                num_4_depth_2 = 0;
                num_5_depth_1 = 0;
                num_5_depth_2 = 0;
                mega_depth_1 = 0;
                mega_depth_2 = 0;
                
                def printDepth(self):
                    print('{0} {1} pick[{2}({3}) {4}({5}) {6}({7}) {8}({9}) {10}({11})] mega[{12}({13})]'.format(
                        self.draw_id,
                        self.date,
                        self.num_1_depth_1,
                        self.num_1_depth_2,
                        self.num_2_depth_1,
                        self.num_2_depth_2,
                        self.num_3_depth_1,
                        self.num_3_depth_2,
                        self.num_4_depth_1,
                        self.num_4_depth_2,
                        self.num_5_depth_1,
                        self.num_5_depth_2,
                        self.mega_depth_1,
                        self.mega_depth_2))
                
                def get_pd1_array(self):
                    pd1_array = [self.num_1_depth_1, self.num_2_depth_1, self.num_3_depth_1, self.num_4_depth_1, self.num_5_depth_1];
                    pd1_array.sort(key=None, reverse=False);
                    
                    pd1_array.insert(0, self.date);
                    pd1_array.insert(0, self.draw_id);
                    
                    pd1_array.append(self.mega_depth_1);
                
                    return pd1_array;
                
                def __init__(self, draw_id):
                    self.draw_id = draw_id;
