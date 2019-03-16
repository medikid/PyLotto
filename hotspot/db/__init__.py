from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from _overlapped import NULL



class db_init():
    db_engine='';
    session='';
    db_user='root';
    #db_pword='';
    #db_host='localhost'    
    db_port=3306
    db_name='lotto_hotspot'
    
    db_pword='admin'
    db_host='192.168.0.100'
    
    def __init__(self):
        self.init_db_engine();
        self.init_session();
        
    def init_db_engine(self):
        #self.db_engine = create_engine('mysql+mysqldb://'+self.db_user+':@'+self.db_host+'[:'+self.db_port+']/'+self.db_name);
        #self.db_engine = create_engine('mysql://root@localhost/lotto_hotspot');
        self.db_engine = create_engine('mysql://admin:admin@192.168.0.100:3306/lotto_hotspot');
  
    
    def init_session(self):
        Session = sessionmaker(bind=self.db_engine);
        self.session = Session();       