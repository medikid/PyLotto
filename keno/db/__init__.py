from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from _overlapped import NULL



class db_init():
    db_engine='';
    session='';
    db_user='root';
    db_pword='';
    db_host='localhost'
    db_port=3306
    db_name='lotto_keno'
    
    def __init__(self):
        self.init_db_engine();
        self.db_engine.echo = False;
        self.init_session();
        
    def init_db_engine(self):
        #self.db_engine = create_engine('mysql+mysqldb://'+self.db_user+':@'+self.db_host+'[:'+self.db_port+']/'+self.db_name);
        self.db_engine = create_engine('mysql://root@localhost/lotto_keno');
  
    
    def init_session(self):
        Session = sessionmaker(bind=self.db_engine);
        self.session = Session();       