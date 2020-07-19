from datetime import datetime
from pytz import timezone

class Utils:
    _LOCAL_TIMEZONE = timezone('America/Los_Angeles')
    
    @staticmethod
    def parseDateTime(date="15-Nov-2017 10:12 PM",date_format='%d-%b-%Y %I:%M %p'):
        dttm = datetime.strptime(date,date_format);
        return dttm

    @staticmethod
    def getTimeStampID(dt_format="%Y%m%d%H%M%S"):
        local_timestamp = Utils.getLocalTimeStamp();        
        return local_timestamp.strftime(dt_format)
    
    @staticmethod
    def getLocalTimeStamp():
        return datetime.now(Utils._LOCAL_TIMEZONE)
    
    @staticmethod
    def convertDatetimeToLocal(DatetimeObj):
        return DatetimeObj.replace(tzinfo=Utils._LOCAL_TIMEZONE)
   

     