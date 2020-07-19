import certifi
import urllib3
import numpy
from bs4  import BeautifulSoup
from utils import Utils
import time

import re
import csv

from bs4 import BeautifulSoup
from dateutil.parser import parse

from superlotto.models import iresult, ipick
from nbconvert.exporters.base import export
from superlotto.models.iresult import iResult
#from keno.fetcher import Fetcher

import pandas as pd

class Fetcher():
    
    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    
    def fetch_results(self, StartID=3368, StartDate='2020-07-10'):
        str_url = "https://www.lotteryusa.com/california/super-lotto-plus/year"
        start_id = StartID
        res = list();

        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        response = http.request('GET', str_url)
        doc = BeautifulSoup(response.data, 'html.parser');
        for tr in  doc.findAll("tr",{"class":"c-game-table__item"}):
            #print(tr)
            try:
                str_draw_dt = tr.find("time",{"class":"c-game-table__game-date"}).get('datetime');
                str_draw_dttm = str_draw_dt + ' 00:00'
                draw_dttm = Utils.parseDateTime(str_draw_dttm, '%Y-%m-%d %H:%M')
                lis = tr.find("ul",{"class":"c-result c-result--in-card c-result--has-extra"}).findAll('li',{"class":"c-result__ball"});
                lis_mega = tr.find("span",{"class":"c-result__ball c-result__ball--blue"});
                num=[]
                for li in lis:
                    num.append(int(li.get_text()));
                    
                mega = int(lis_mega.get_text());

                #print('{0}[{1}][{2}]'.format(draw_dttm,num,mega))
                res.append([start_id, draw_dttm, num[0],num[1],num[2],num[3],num[4], mega])
                
                
                start_id += 1;
            except:
                pass;
        
        
        res_ev_df = pd.DataFrame(res, columns=['draw_id','draw_dttm','r1','r2','r3','r4','r5','mega'])        
        res_df = res_ev_df.sort_values(by=['draw_dttm'])
        print(res_df)
            
        return res_df;
    
    def get_results(self):
        self.result_file_url = "https://www.calottery.com/sitecore/content/Miscellaneous/download-numbers/?GameName=powerball&Order=Yes"
        self.draws_file_csv = "E:/Projects/Lotto/powerball/Results/Draws.csv"
        
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        response = http.request('GET', self.result_file_url)
        page_html = response.data.decode('utf-8')
        
        results = []
        for line in page_html.split("\n"):
            lines=[]
            for word in line.split(" "):
                if  len(word) > 0 and word !="\r":
                    lines.append(word);
                    print(word)
            results.append(lines)
            
        
        
        results.pop(0);results.pop(1);results.pop(2);results.pop(3);results.pop(4);results.pop(5);results.pop(6);results.pop(7);
        draws=results;
        out = csv.writer(open(self.draws_file_csv,"w", newline=''), delimiter=',',quoting=csv.QUOTE_ALL)
        out.writerow(["draw_id", "week_day", "mon", "day", "year", "num_1", "num_2", "num_3", "num_4", "num_5", "mega"]);
                
        for i in range(len(draws)):
            out.writerow(draws[i]);
                        
        print(*draws)
        return page_html;
    
    
    def read_CSV(self):
        self.csv_file="E:/Projects/Lotto/powerball/Results/Draws.csv"
        with open(self.csv_file) as CSV_FILE:
            in_file = csv.reader(CSV_FILE, delimiter=',')
            for row in in_file:
                res = iresult.iResult(row[0], time.strptime(row[1], '%d-%b-%Y'), [row[2], row[3],row[4],row[5],row[6]], row[7])
                res.db_save()
 
    
    def fetch_result_old(self, DrawID):
        url="https://www.californialottery.com/sitecore/content/LotteryHome/play/draw-games/hot-spot/draw-detail?draw=";
        url_str=url+str(DrawID);
        
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        http = urllib3.PoolManager()
        #http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED')
        response = http.request('GET', url_str)
        doc = BeautifulSoup(response.data, 'html.parser');
        drw = doc.find("h3",{"class":"hotspot-callout-text"});
        draw_id=drw.get_text().strip()

        
        uls = doc.find("ul", {"id": "hotSpotDrawResults"});
        lis = uls.find_all("li")
        dttm = doc.find("div", {"class":"hotspot-details-datetime"}).find_all("p")
        pick_array=[]
        pick_mega=0;
        for li in lis:
            li_cls = li.get('class');
            if (len(li_cls)>1):
                pick_array.append(li.get_text())
                if (len(li_cls)>2): pick_mega=li.get_text(); print("bonus",li.get_text());
        
        date = dttm[0].get_text().split(":")[1]
        wk_day=date.split(",")[0].strip()
        month=date.split(",")[1].strip().split(" ")[0].strip()
        day=date.split(",")[1].strip().split(" ")[1].strip()
        year=date.split(",")[2].strip().strip()
        time_hr=dttm[1].get_text().split(":")[1].strip()
        time_min=dttm[1].get_text().split(":")[2].split(" ")[0].strip()
        am_pm=dttm[1].get_text().split(":")[2].split(" ")[1].strip()
        
        str_dttm=day+'-'+month+'-'+year+' '+time_hr+':'+time_min+' '+am_pm;
        draw_date_time=Utils.parseDateTime(str_dttm)
        pick=ipick.iPick(pick_array)
        print("date",str_dttm, pick.toString())
        print(drw.get_text().strip())
        r = iresult.iResult(draw_id, draw_date_time,pick , pick_mega )
        return r;
        #dttm = dttm_p.select("p")get;
#         lis = uls.select("li");
#         swin = "spot win";
#         swbonus = "spot win bonus";

#         print("parsed draw ID: " + drw.text());
#             draw_array[0]=drw.text(); System.out.println(drw.text());
#             draw_array[1]=dttm.select("p").text();
#             
#             //Date draw_date = utils.getDateTimeFromHTML(dttm.select("p").text());
#             
#             //System.out.println(dttm.select("p").text());
#             String mega = null;
#             int i = 2;
#             for (Element li:lis){
#                 if (li.className().equals(swin)){
#                     //System.out.println(li.text());
#                     draw_array[i]=li.text();
#                     i++;
#                 } else if (li.className().equals(swbonus)){
#                     //System.out.println(li.text());
#                     draw_array[i]=li.text();
#                     mega = li.text();
#                     i++;
#                 }
#                 
#             }
#             draw_array[i] = mega;    
#             
#         } catch (IOException e) {
#             // TODO Auto-generated catch block
#             e.printStackTrace();
#         }

#         return draw_array;

    def fetch_results_old(self, start_id, end_id):
        draw_id = start_id;
        while(draw_id < end_id):
            res = self.fetch_result(draw_id);
            res.db_save();
            draw_id += 1;
    
    def sync_results(self):
        res = iresult.iResult();
        last_draw_id=res.getLastDrawID();
        next_draw_id = last_draw_id + 1;
        #print(last_draw_id)
        while(True):
            new_res = self.fetch_result(next_draw_id)
            new_res.db_save()
            next_draw_id += 1;


# f = Fetcher()
# f.get_results()
# f.read_CSV()
# f.sync_results()
# f.fetch_results(2357100, 2357100) #2381149)
