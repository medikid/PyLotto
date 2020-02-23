import urllib3, certifi, requests
from bs4  import BeautifulSoup
from utils import Utils

from keno.models import iresult, ipick
from keno.db import db_init;
from keno.db.db_base import DBBase

import csv, io, zipfile

certifi, requests

import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class Fetcher():
    db = db_init();
    
    def get_zip_files_by_url(self, z_url):
        #z_url = "http://www.bclc.com/DownloadableNumbers/CSV/KenoCurrentYear.zip"
        #z_url = "http://www.bclc.com/DownloadableNumbers/CSV/KenoPastYears.zip"

        headers= { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
        
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        
        content = requests.get(z_url, verify=False, headers=headers)
        zipfiles = zipfile.ZipFile(io.BytesIO(content.content))
        return zipfiles;

    def read_zipped_csv(self, z_url=None, filename=None):
        zipfiles = self.get_zip_files_by_url(z_url);
        df = pd.read_csv(zipfiles.open(filename));
        results= pd.DataFrame();
        results['draw_id'] = df['DRAW NUMBER'].astype('int64');
        #results['data_time'] = pd.datetime(df['DRAW DATE'], format='%Y-%m-%d %H:%M:%S', errors='ignore');
        results['date_time'] = df['DRAW DATE'].astype('datetime64[ns]');
        i=1;
        while (i <= 20):
            results['r'+str(i)] = df['NUMBER DRAWN ' + str(i)].astype('int64');
            i += 1;
        results['mega'] = df['BONUS MULTIPLIER'].astype('float')
        results.set_index('draw_id', inplace=True)
        results.index = results.index.astype('int64')
        #print(results[results.index >2312060].head())
        return results;

    def upload_dataframe(self, data_frame, table_name='results'):
        # query = (' SELECT MAX(`draw_id`) FROM {}').format(table_name)
        # df = pd.read_sql(query, con=self.db.db_engine)
        # print(df)
        data_frame.to_sql(name=table_name, con=self.db.db_engine, if_exists='append', index=True)


    def fetch_online_csv(self):
        cur_year_zip = "http://www.bclc.com/DownloadableNumbers/CSV/KenoCurrentYear.zip"
        prev_years_zip = "http://www.bclc.com/DownloadableNumbers/CSV/KenoPastYears.zip"

        cur_file_name = 'KenoCurrentYear.csv'
        prev_file_name = 'KenoYear2019.csv'

        results = self.read_zipped_csv(cur_year_zip, cur_file_name);
        #results = self.read_zipped_csv(prev_years_zip, prev_file_name);

        #print(results[results.index >2312063].head())

        self.upload_dataframe(results, 'results')

        return results[results.index >2312063]
    
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