from hotspot import HotSpot, fetcher;
from hotspot.models import iticket, iprize, isession
from hotspot.controllers import prizes
import os, ssl

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

h = HotSpot();
#h.sync()
#.setupTickets();

p = prizes.Prizes();
p.setup_prize_list()
prz = p.get_prize(10,5);
print("Prize ID", prz.prz_id,": ", prz.prize);

#h.derive_draws(2439018, 2494108);
#h.derive_depths(2439018, 2494107)
#h.find_gaps_results(2277311, 2494108);
#h.find_gaps_draws(2277311, 2494108)
#h.find_gaps_depths(2277311, 2494108)

#print("Last Draw: ", h.get_last_draw_id());