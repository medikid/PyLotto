import certifi
import urllib3
from bs4  import BeautifulSoup
from utils import Utils

from dailyderby.models import iresult
from nbconvert.exporters.base import export
import datetime, time

import re
import pandas as pd
#from keno.fetcher import Fetcher


class Fetcher():
    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def fetch_results(self, StartID=1234, StartDate='2020-07-10'):
        draw_id = StartID;
        url_str="https://www.lotteryusa.com/california/daily-derby/year";
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        response = http.request('GET', url_str)
        doc = BeautifulSoup(response.data, 'html.parser');
        res = list();

        for tr in  doc.findAll("tr",{"class":"c-game-table__item"}):
            try:
                str_draw_dt = tr.find("time",{"class":"c-game-table__game-date"}).get('datetime');
                str_draw_dttm = str_draw_dt + ' 00:00'
                draw_dttm = Utils.parseDateTime(str_draw_dttm, '%Y-%m-%d %H:%M')
                lis = tr.find("ul",{"class":"c-result c-result--in-card"}).findAll('li');
                for li in lis:
                    result = li.get_text();
                    first = re.search('1st:(.+?)2nd:',result).group(1).strip()[:2]
                    second = re.search('2nd:(.+?)3rd:',result).group(1).strip()[:2]
                    third = re.search('3rd:(.+?)RaceTime:', result).group(1).strip()[:2]
                    racetime = re.search('RaceTime: (.+:?)',result).group(1).strip()
                    i_racetime = int(racetime.split(':')[1][1:2] + racetime.split(':')[1][3:])
                res.append([draw_id, draw_dttm, int(first), int(second), int(third), racetime, i_racetime])
                #print('{0}[{1} {2} {3}][{4}[{5}]'.format(draw_dttm,first, second, third,racetime, i_racetime))
                draw_id +=1;
            except:
                try:
                    first = re.search('1st:(.+?)2nd:',result).group(1).strip()[:2]; #print(first)
                    second = re.search('2nd:(.+?)3rd:',result).group(1).strip()[:2]; #print(second)
                    third = re.search('3rd:(.+?)Race Time:', result).group(1).strip()[:2]; #print(third)
                    racetime = re.search('Race Time:(.+:?)',result).group(1).strip(); #print(racetime)
                    i_racetime = int(racetime.split(':')[1][1:2] + racetime.split(':')[1][3:]); #print(i_racetime)                  
                    res.append([draw_id, draw_dttm, int(first), int(second), int(third), racetime, i_racetime])
                    #print('E{0}[{1} {2} {3}][{4}[{5}]'.format(draw_dttm,first, second, third,racetime, i_racetime))
                    draw_id+=1;
                except:
                    print("Could not parse")
                    pass;

        res_ev_df = pd.DataFrame(res, columns=['draw_id', 'draw_dttm','r1','r2','r3','rt','i_rt'])

        res_df = res_ev_df.sort_values(by=['draw_dttm'])

        return res_df;