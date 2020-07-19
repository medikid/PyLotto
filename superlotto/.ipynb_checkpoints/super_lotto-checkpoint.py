import urllib3;
import certifi;
import re
import csv

from bs4 import BeautifulSoup
from dateutil.parser import parse
import MySQLdb



class SuperLotto:
    draws_url = "http://www.calottery.com/play/draw-games/superlotto-plus/winning-numbers"
    draws_file_url = "http://www.calottery.com/sitecore/content/Miscellaneous/download-numbers/?GameName=superlotto-plus&Order=No"
    draws_file = "E:/Projects/Lotto/superlotto/Results/Draws.txt"
    draws_file_csv = "E:/Projects/Lotto/superlotto/Results/Draws.csv"
    pickdepth_file_csv = "E:/Projects/Lotto/superlotto/Results/PickDepth.csv"
    draws = [];
    picks=[];
    is_draws_loaded = False;   
    db = MySQLdb.connect('localhost','root',"mysql",'superlotto');
    db_cur = db.cursor();
        
    def __init__(self):
        
        if(self.is_draws_loaded == False):
            self.parse_draws();
            self.set_draws_loaded();
    
    def set_draws_loaded(self):
        self.is_draws_loaded = True;
    
    def parse_draws(self):
        page_html = self.get_draws();
        self.write_draws(page_html);
        self.load_draws();
        self.set_draws_loaded();
    
    def get_draws(self):
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        response = http.request('GET', self.draws_file_url)
        page_html = response.data.decode('utf-8')
        return page_html;
    
    def write_draws(self, page_html):
        soup = BeautifulSoup(page_html, "html.parser")
        open(self.draws_file, "wb").write(soup.prettify().encode('utf-8'))
        
    def write_results_csv(self):
        draws = self.get_draws_array();
        out = csv.writer(open(self.draws_file_csv,"w", newline=''), delimiter=',',quoting=csv.QUOTE_ALL)
        out.writerow(["draw_id", "date", "day", "num_1", "num_2", "num_3", "num_4", "num_5", "mega"]);
                
        for i in range(len(draws)):
            out.writerow(draws[i].get_array());   
    
    def load_draws(self):
        with open(self.draws_file,'rb') as f:
            w = f.readlines();
        
        for i in range(len(w)):
            if i>4:
                self.draws.append(self.Draw(w[i].decode('utf-8').split()));
            #print(w[0].decode('utf-8'))
            #self.results.append(self.SuperLottoResult());
        #print(self.draws[2].db_upload_draw());
        
    def db_upload_draws(self):
        self.draws.reverse();
        for i in range(len(self.draws)):
            if self.db_drawid_exist(self.draws[i].draw_id)==False:
                self.draws[i].db_upload_draw();
                
        
   
    
    def print_draw(self, index):
        print(self.draws[index].print_draw());
    
    def get_draw_by_draw_id(self, DrawID):
        for i in range(len(self.draws)):
            if(self.draws[i].draw_id == DrawID):
                self.draws[i].print_draw()
                
    def get_draws_array(self):
        return self.draws;
    
    def connect(self):        
        query_txt = "SELECT * FROM `draws` WHERE 1";
        self.db.execute(query_txt);
        for rows in self.db.fetchall():
            print(rows);
        
    def db_drawid_exist(self, drawID):
            draw_id_exist = False;
            query_txt = "SELECT * FROM `superlotto`.`draws` WHERE `draw_id`= ";
            query_txt += str(drawID);
            self.db_cur.execute(query_txt);
            row_count = self.db_cur.rowcount;
            if (row_count > 0):
                draw_id_exist = True;
            
            return draw_id_exist;    
    
    
    def db_insert(self):
        #cur = self.db.cursor();
        query_txt = "INSERT INTO `superlotto`.`draws` (`draw_id`, `draw_date`, `draw_day`, `num_1`, `num_2`, `num_3`, `num_4`, `num_5`, `mega`) VALUES ('2', '2000-01-01', 'Mon', '1', '2', '3', '4', '5', '55')";
        self.db_cur.execute(query_txt);
        self.db.commit();
        
        
    def select(self):
        query_txt = "SELECT * FROM `draws` WHERE 1";
        
        
           
    class Draw(object):
        draw_id = 0;
        week_day = 0;
        day = 0;
        month = 0;
        year = 0;
        num_1 = 0;
        num_2 = 0;
        num_3 = 0;
        num_4 = 0;
        num_5 = 0;
        mega = 0;
        db = MySQLdb.connect('localhost','root',"mysql",'superlotto');
        db_cur = db.cursor();
        
        
        r_array = [];
        
        def __init__(self,w):
            self.draw_id = int(w[0]);
            self.week_day = w[1].replace(".","");
            self.day = int(w[3].replace(",","")); self.month = w[2]; self.year = int(w[4]);
            self.num_1 = int(w[5]); self.num_2 = int(w[6]); self.num_3 = int(w[7]); self.num_4 = int(w[8]); self.num_5 = int(w[9]);
            self.mega = int(w[10]);
            #self.print_result()
                    
        def get_date(self):
            return str(self.day)+"-"+str(self.month)+"-"+str(self.year);
        
        def get_array(self):
            self.r_array = [self.draw_id, self.get_date(), self.week_day, self.num_1, self.num_2, self.num_3, self.num_4, self.num_5, self.mega];
            return self.r_array;
        
        def print_draw(self):
            print('{0}. {1}-{2}-{3}({4}) [{5} {6} {7} {8} {9}][{10}]'.format(self.draw_id, self.day,self.month,self.year,self.week_day,self.num_1, self.num_2, self.num_3, self.num_4, self.num_5,self.mega))
           
        def load_draw(self, drawID):
            pass;
        
        def validate_pick(self, pick):
            if(pick.num_1 in self.draw_set):
                pick.draw.set_num_match();
            if(pick.num_2 in self.draw_set):
                pick.draw.set_num_match();
            if(pick.num_3 in self.draw_set):
                pick.draw.set_num_match();
            if(pick.num_4 in self.draw_set):
                pick.draw.set_num_match();
            if(pick.num_5 in self.draw_set):
                pick.draw.set_num_match();
                
            if(pick.mega in self.draw_set):
                pick.draw.set_mega_match();
                
            pick.validated = True;
        
            return pick;
        
        def get_db_draw_date(self):
            return parse(self.get_date()).strftime("%Y-%m-%d");
        
        def db_upload_draw(self):
            query_txt = "INSERT INTO `superlotto`.`draws` (`draw_id`, `draw_date`, `draw_day`, `num_1`, `num_2`, `num_3`, `num_4`, `num_5`, `mega`)";
            #query_txt += " VALUES ('{0}', '{1}', "'{2}'", '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')";
            query_txt += " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)";
            
            self.db_cur.execute(query_txt, (self.draw_id, self.get_db_draw_date(), self.week_day, self.num_1, self.num_2, self.num_3, self.num_4, self.num_5, self.mega));
            self.db.commit();
        
       
        
    class Result(object):
        
        def set_num_match(self):
            self.num_match += 1;
            
        def unset_num_match(self):
            self.num_match -= 1;
            
        def set_mega_match(self):
            self.mega_match += 1;
            
        def unset_mega_match(self):
            self.mega_match -= 1;
            
        def get_result(self):
            return [self.num_match, self.mega_match];
        
        def print_result(self):
            print('PickID:{}({}) - Match[{},{}]'.format(self.num_match, self.mega_match))
    
        def __init__(self, DrawID):
            self.draw_id = DrawID;
            self.num_match =0;
            self.mega_match=0;
        
   
    class Pick(object):
        pick_id = 0;
        draw_id = 0;
        version_id = 0;
        num_1 =0;
        num_2 =0;
        num_3 =0;
        num_4=0;
        num_5=0;
        mega=0;
        validated=False;
        
        
        def __init__(self, drawID, pickID, versionID, pArray):
            self.pick_id = pickID;            
            self.draw_id = drawID;
            self.version_id = versionID;
            self.num_1 = pArray[0]; self.num_2 = pArray[1]; self.num_3 = pArray[2]; self.num_4 = pArray[3]; self.num_5 = pArray[4];
            self.mega = pArray[5]
            
            self.result = self.Result(self.draw_id);
                    
        def set_validated(self):
            self.validated = True;
            
        def print_result(self):
            if(self.validated):
                print('PickID:{}({}) - Match[{},{}]'.format(self.pick_id, self.draw_id, self.num_match, self.mega_match));
            else:
                print('Pick ID:{}({}) - Unvalidated'.format(self.pick_id, self.draw_id));
    