#all the fixes 

#unable to connect mysql running in docker - KEYERROR 255

#//replaced on 1268 pymysql/connection.py
#self.server_charset = charset_by_id(lang).name
            #//// replaced to fix KEY ERROR 255
            #try:
                #self.server_charset = charset_by_id(lang).name
            #except KeyError:
                #self.server_charset = None
            #/////



# tx_isolatioon is replaced by transaction_isolation
#/replaced line 1569 sqlalchemy/dialetcts/base.py
#('SELECT @@tx_isolation') #replaced tx_isolation with transaction_isolation