from datetime import datetime as dt
from datetime import time
import pandas as pd

#hotspot
#02:00 - last, -06:04 is first every 4 min

#keno
#4:00 - last, 5:04:30 first every 3:30 min

class FillGaps():

    def __init__(self):
        pass

    def generate(self):
        times = pd.date_range('2012-10-01', periods=289, freq='5min');
        print(times)

        perdaymin = 24 * 60
        perday5min = perdaymin/5
        perday4min = (perdaymin-4)/4
        perday330min = (perdaymin-1)/3.5
        print("Per Day: %i" % perdaymin)
        print("Periods with 5 min: %i " % perday5min)
        print("Periods with 4 min: %i " % perday4min)
        print("Periods with 330 min: %i " % perday330min)

        pass;

    def generate_hotspot(self):
        times = pd.DataFrame();
        #times['dt'] = pd.date_range(start='2017-05-09 22:36', end='2020-01-18 04:00', freq='4min');
        times['dt'] = pd.date_range(start='2018-03-23 19:20:00', end='2018-06-04 00:00', freq='4min');

        #times['time'] = times['dt'].apply(lambda x: (self.extract_time(x)))
        times['time'] = times.apply(lambda x: x['dt'].time(), axis=1)
        times['keep'] = times.apply(lambda x: "Yes" if x['time'] > time(6,0,0) or x['time'] <= time(2,0,0) else "No", axis=1 )

        #times.drop(times[times.keep == "No"].index, inplace=True)
        times.drop(times[ (times['dt'].apply(lambda x: x.time()) <= time(6,0,0)) & (times['dt'].apply(lambda x: x.time()) > time(2,0,0)) ].index, inplace=True)

        times['draw_id'] = times.apply(lambda x: x.name + 2372662, axis=1)
        
        WRITER = pd.ExcelWriter(r'Y:/rancheros/eclipse/instance/data/workspaces/workspace4i8ynyxq64yvcgk8/medikid-PyLotto/data/reports/times2.xlsx', engine='xlsxwriter')
        times.to_excel(WRITER, sheet_name='trial')
        WRITER.save();


        # tm = time(5,4);
       
        # print(tm)

        # for i in times['dt']:
        #     print(i.time())

    def extract_time(self, column):
        return column.time();
    
    def generate_keno(self):
        times = pd.date_range(start='2020-01-17 05:03:30', end='2020-01-17 05:03:30', periods=360, freq='3.5min');
        #print(times)
       


    def parseDateTime(self, date="15-Nov-2017 10:12 PM",date_format='%d-%b-%Y %I:%M %p'):
        dttm = dt.strptime(date,date_format);
        return dttm

    def getTimeStamp(self, dt_format="%Y%m%d%H%M%S"):
        date_time = dt.now();
        
        return date_time.strftime(dt_format)
   