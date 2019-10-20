import certifi
import urllib3
from bs4  import BeautifulSoup
from utils import Utils

from hotspot.models import iresult, ipick
from nbconvert.exporters.base import export
import datetime
#from keno.fetcher import Fetcher


class Fetcher():

    def fetch_result(self, DrawID):
        #url="https://www.californialottery.com/sitecore/content/LotteryHome/play/draw-games/hot-spot/draw-detail?draw=";
        url="https://www.calottery.com/play/draw-games/hot-spot/draw-detail?draw=";
        
        new_url="https://www.calottery.com/draw-games/hot-spot/past-winning-numbers?query="
        
        url_str=new_url+str(DrawID);
        
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        #http = urllib3.PoolManager()
      
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        response = http.request('GET', url_str)
        doc = BeautifulSoup(response.data, 'html.parser');
        
        drw = doc.find("div",{"class":"card-body"});
        dttm = drw.find("p",{"class":"htspt__cards--next-draw-date"}).get_text().strip().split(":")
        date=dttm[1].split("\n")[0].strip()
        time_hr="{:02d}".format(int(dttm[2]))
        time_mn_am=dttm[3].split(" ")
        time_mn=time_mn_am[0]
        time_ampm=time_mn_am[1].split(".")
        time_AMPM=time_ampm[0].upper()+time_ampm[1].upper()
        str_dttm = date + " " +time_hr +":"+ time_mn +" " + time_AMPM
        dttm_format="%B %d, %Y %I:%M %p"
        
        draw_date_time = Utils.parseDateTime(str_dttm, dttm_format)
        
        uls = drw.find("ul", {"class": "list-inline"});
        lis = uls.find_all("li", {"class": "list-inline-item blue-num"});
        lis_bonus = uls.find("li", {"class": "list-inline-item yellow-num"});
        
        pick_array=[]
        pick_mega=0;
        for li in lis:            
            pick_array.append(int(li.get_text()))
        
        pick_mega=int(lis_bonus.get_text());
        pick_array.append(int(pick_mega))
        print(draw_date_time, pick_array, "bonus",pick_mega);
        
        pick=ipick.iPick(pick_array)
        r = iresult.iResult(DrawID, draw_date_time, pick , pick_mega )
        return r;

    
    def fetch_result_old(self, DrawID):
        #url="https://www.californialottery.com/sitecore/content/LotteryHome/play/draw-games/hot-spot/draw-detail?draw=";
        #url="https://www.calottery.com/play/draw-games/hot-spot/draw-detail?draw=";
        
        new_url="https://www.calottery.com/draw-games/hot-spot/past-winning-numbers?query="
        
        url_str=new_url+str(DrawID);
        
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        #http = urllib3.PoolManager()
      
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
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

    def fetch_results(self, start_id, end_id):
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
        
    
f = Fetcher()
#f.sync_results()
#f.fetch_results(2357100, 2357100) #2381149)
