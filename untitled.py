from daily3 import fetcher;
#from hotspot.models import iticket, iprize, isession
#from hotspot.controllers import prizes
import os, ssl

#setup by sudo python boot_strap.py
#run py in background - nohup python main.py &
#find main.py process - ps ax | grep main.py
#kill pid - kill pid or pkill -f main.pypyno

#if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
#   ssl._create_default_https_context = ssl._create_unverified_context;

#os.environ['REQUESTS_CA_BUNDLE'] = os.path.join('/etc/ssl/certs/','ca-certificates.crt')
ssl._create_default_https_context = ssl._create_unverified_context
#f = fetcher.Fetcher();
#f.fetch_results(2491604, 2494106)  #start=2438718 end=2492927;
#f.get_results();

f = fetcher.Fetcher();
f.fetch_results()