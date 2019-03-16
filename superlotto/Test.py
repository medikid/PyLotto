from bs4 import BeautifulSoup
import urllib3.request
import certifi
from pprint import pprint
from SuperLotto.super_lotto import SuperLotto
from SuperLotto.num_pick import NumPick
from SuperLotto.pick_depth import PickDepth

from dateutil.parser import parse

url_r_file = "http://www.calottery.com/sitecore/content/Miscellaneous/download-numbers/?GameName=superlotto-plus&Order=No"
url_r_page = "http://www.calottery.com/play/draw-games/superlotto-plus/winning-numbers"


http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
response = http.request('GET', url_r_file)
page_html = response.data.decode('utf-8')

soup = BeautifulSoup(page_html, "html.parser")
open("E:/soup.txt", "wb").write(soup.prettify().encode('utf-8'))

with open('E:/soup.txt','rb') as f:
    lines = f.readlines()


sl = SuperLotto();
sl.write_results_csv();
#sl.load_draws();
date = '1-Apr-2017'
print(parse(date).strftime("%Y-%m-%d"))
print(sl.db_drawid_exist(3131));

sl.db_upload_draws();
#sl.db_insert();
#pd = PickDepth(sl);
#np = NumPick(sl);
#np.calc_probs(10, 1);


#pd.write_results_csv();
#sl.get_result_by_draw_id(3000)
#pd.get_pick_depth(3115)
#pd.write_pick_depth_csv();
#pd.read_pick_depth_csv()


# for i in range(5,6):
#     print( i,".", lines[i],"\n" );
