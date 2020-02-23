from datetime import datetime

class Utils:
    
    @staticmethod
    def parseDateTime(date="15-Nov-2017 10:12 PM",date_format='%d-%b-%Y %I:%M %p'):
        dttm = datetime.strptime(date,date_format);
        return dttm

    @staticmethod
    def getTimeStamp(dt_format="%Y%m%d%H%M%S"):
        date_time = datetime.now();
        
        return date_time.strftime(dt_format)
   

     