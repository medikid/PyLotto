import certifi
import urllib3
from bs4  import BeautifulSoup
from utils import Utils

#from hotspot.models import iresult, ipick
from nbconvert.exporters.base import export
import datetime, time

import pandas as pd
#from keno.fetcher import Fetcher


class Fetcher():
    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def fetch_results(self):
        midday_url_str="https://www.lotteryusa.com/california/midday-3/year";
        evening_url_str="https://www.lotteryusa.com/california/daily-3/year";
        midday_draw_time= "13:30";
        evening_draw_time= "18:30"
        
        res_md = self.fetch(midday_url_str, midday_draw_time);
        res_ev = self.fetch(evening_url_str, evening_draw_time);
        
        res_md_df = pd.DataFrame(res_md, columns=['draw_dttm','r'])
        res_ev_df = pd.DataFrame(res_ev, columns=['draw_dttm','r'])
        res_us_df = res_md_df.append(res_ev_df)
        res_df = res_us_df.sort_values(by=['draw_dttm'])
        
        return res_df
        
    def fetch(self, url, draw_time):
        str_url = url;
        str_draw_time = draw_time
        res = list();

        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        response = http.request('GET', str_url)
        doc = BeautifulSoup(response.data, 'html.parser');
        for tr in  doc.findAll("tr",{"class":"c-game-table__item"}):
            try:
                str_draw_dt = tr.find("time",{"class":"c-game-table__game-date"}).get('datetime');
                str_draw_dttm = str_draw_dt + ' ' + str_draw_time
                draw_dttm = Utils.parseDateTime(str_draw_dttm, '%Y-%m-%d %H:%M')
                lis = tr.find("ul",{"class":"c-result c-result--in-card"}).findAll('li');
                num=''
                for li in lis:
                    num += li.get_text()

                #print('{0}[{1}]'.format(draw_dttm,num))
                res.append([draw_dttm, int(num)])
            except:
                pass;
            
        return res;