import urllib3
from bs4  import BeautifulSoup
from utils import Utils

from keno.models import iresult, ipick
import csv, io

class Fetcher():
    
    def fetch_csv_results(self):
        data_folder='../results/';
        csvFileList=[];
        i=2002;
        while(i<2019):
            csvFileList.append("YR"+str(i)+"AKENO.csv");
            csvFileList.append("YR"+str(i)+"BKENO.csv");
            i+=1
        
        for csvFileName in csvFileList:
            path=data_folder+csvFileName;
            self.fetch_csv_file(path);
            
        
    
    def fetch_csv_file(self, csv_path):
        with io.open(csv_path, 'r', encoding='utf8') as csvFile:
        #for tweet in f.readlines():
        #    tweet = tweet.strip()
#         with open(csv_path, newline='') as csvFile:
#         #with open('../results/YR1995BKENO.csv','r') as csvFile:
#             csvreader = csv.reader(csvFile, delimiter=' ', quotechar='|')
#             
            header=csvFile.readline()
            for rows in csvFile.readlines():
                row = rows.strip()
                columns = row.split(',')
                r = iresult.iResult();
                r.draw_id = int(columns[1])
                r.date_time = Utils.parseDateTime(columns[2], '=\"%d/%m/%Y %H:%M:%S\"')
                r.numFromArray([int(columns[4]), int(columns[5]), int(columns[6]), int(columns[7]), int(columns[8]), int(columns[9]), int(columns[10]), int(columns[11]), int(columns[12]), int(columns[13]), int(columns[14]), int(columns[15]), int(columns[16]), int(columns[17]), int(columns[18]), int(columns[19]), int(columns[20]), int(columns[21]), int(columns[22]), int(columns[23])]);r.mega = columns[3];
                if(columns[3]==''):r.mega=0;
                else: r.mega=float(columns[3]);
                r.db_save()
                
    def fetch_result(self, DrawID):
        url="http://www.californialottery.com/sitecore/content/LotteryHome/play/draw-games/hot-spot/draw-detail?draw=";
        url_str=url+str(DrawID);
        
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        http = urllib3.PoolManager()
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
        print(last_draw_id)
        while(True):
            new_res = self.fetch_result(next_draw_id)
            new_res.db_save()
            next_draw_id += 1;
        
    
f = Fetcher();
data_folder='../results/';
fileName = data_folder+"YearlyBKENO.csv"
#f.fetch_csv_file(fileName)
#f.fetch_csv_results();