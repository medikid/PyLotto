from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from _overlapped import NULL



class db_init():
    db_engine='';
    session='';
 
    
    #db_host='localhost'
    db_host='192.168.0.111'
    
    db_user='db_user'
    db_pword='db_pwd'

    # db_user='root'
    # # db_pword=''
    # db_pword = 'lubdub'
    
    db_port= 3306
    db_name='lotto_hotspot'
    

    #charset='UTF8MB4'

    def __init__(self):
        self.init_db_engine();
        self.init_session();
        
    def init_db_engine(self):
        #print('mysql+mysqldb://'+self.db_user+':'+self.db_pword+'@'+self.db_host+':'+str(self.db_port)+'/'+self.db_name)
        self.db_engine = create_engine('mysql+mysqldb://'+self.db_user+':'+self.db_pword+'@'+self.db_host+':'+str(self.db_port)+'/'+self.db_name);
        #self.db_engine = create_engine('mysql+mysqldb://db_user:db_pwd@192.168.0.111:3306/lotto_hotspot');
  
    
    def init_session(self):
        Session = sessionmaker(bind=self.db_engine);
        self.session = Session();       