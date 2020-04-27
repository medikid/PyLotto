from hotspot import HotSpot, fetcher
from hotspot.models import iticket, iprize, isession, iball, ibowl, istrategy, ipreds, iresult, idraw, idepth, index, iexplore, iexplorelog, ireport
from hotspot.controllers import prizes
from hotspot.explore import Explore
from hotspot.explore.algos import prev_wins, diag_2_wins, diag_3_wins, diag_4_wins, depth_0_4, depth_5_10, depth_11_20, depth_21_over
from hotspot.explore.algos import combos_1
from hotspot.reports import depth_summary, data_export, db_validation_report
from hotspot.fill_gaps import FillGaps

from keno.fetcher import Fetcher as kfetcher

import os, ssl

from numpy.random import choice as np_choice
import pandas as pd
import random as r


from session import Session
import timeit
from time import time

# start = time()
#h = HotSpot();

# h.sync(10);
# elapsed = time() - start;
# print("Took sync(10) time %i secs " % elapsed )

# # #print(h.get_last_draw_id())
# # #h.find_gaps_results(1,2549397)
# # #h.find_gaps_draws(1,2549397)
# # #h.find_gaps_depths(1,2549397)
#h.find_gaps();

# k = kfetcher();
# #k.fetch_online_csv()
# k.upload_dataframe(1)

f = fetcher.Fetcher();
df = f.sync_results_df();
print(df)

######DEPTH#############
# rs = iresult.iResult();
# df_rs = rs.get_dataframe();

# dr= idraw.iDraw();
# df_dr = dr.get_dataframe();

# dp = idepth.iDepth();
# df_dp = dp.get_dataframe();
# df_dp_x = pd.DataFrame();
# #df_dp_x = dp.get_dataframe(['draw_id'],['<'],['2277320']);
# df_dp_x['draw_id'] = df_dp['draw_id']
# #n1_col = df_dp_x.columns.get_loc('n5');
# #Eprint(df_dp_x[df_dp_x['n2']==0].index)

# i=1; col = 'n'
# while (i < 81):
#     col_name = col+str(i)
#     #col_ind = df_dp_x.columns.get_loc(col_name)
#     #new_col_name = col_name+"_"
 
#     #df_dp_x.insert(col_ind+1, new_col_name,'')
#     df_dp_x[col_name] = '';
#     #ind_0 = df_dp_x[df_dp_x[col_name]==0].index
#     ind_0 = df_dp[df_dp[col_name]==0].index
#     for i0 in ind_0:
#         if (i0 > 0): #skip first row
#             df_dp_x.at[i0, col_name] = df_dp.at[i0-1, col_name]
#             #df_dp_x.set_value(i0, new_col_name, df_dp_x.at(i0-1, col_name) )
#     i+=1

#file_location = r'Y:/rancheros/eclipse/instance/data/workspaces/workspace4i8ynyxq64yvcgk8/medikid-PyLotto/data/reports/'
#file = file_location + 'lotto_hotspot_depth_summary.xlsx'

#df_dp_x = pd.read_excel(file, sheet_name='depths_summary', index_col=0)
#print(df_dp_x.n1.value_counts())
#dp_sum = df_dp_x.apply(pd.value_counts)
#print(dp_sum)

#WRITER = pd.ExcelWriter(r'Y:/rancheros/eclipse/instance/data/workspaces/workspace4i8ynyxq64yvcgk8/medikid-PyLotto/data/reports/lotto_hotspot_depth_summary.xlsx', engine='xlsxwriter')

# # df_rs.to_excel(WRITER, sheet_name='results')
# # df_dr.to_excel(WRITER, sheet_name='draws')
# # df_dp.to_excel(WRITER, sheet_name='depths')
#df_dp_x.to_excel(WRITER, sheet_name='depths_summary')


#WRITER.save();

### EXPLORE ######
# e = iexplore.iExplore();
# e.xplr_id = 21;
# e.setup();
# i = iexplorelog.ExploreLog();
# i.create_table();

# i = index.Index(None, None, 1);
# for e in i.explores:
#     print(e.xplr_id);
# print(i.idx_id, i.desc)

# p = prev_wins.PREV_WINS();
# p.register_index();


# d=combos_1.COMBOS_1(2566556, 10000, True)

# #d =  depth_21_over.DEPTH_21_OVER(2566556, 10000, True)
# #d = prev_wins.PREV_WINS(2566556, 10000, True);
# #d = diag_2_wins.DIAG_2_WINS(2566556, 1000, True);
# #d = diag_4_wins.DIAG_4_WINS(2566556, 10000, True);
# #d.register_index();
# d.explore(False);
# d.print_summary()

#e = Explore('PREV_WINS', 2566556, 5, True);
# e = Explore("PREV_WINS", 2566556, 10000, True);
# e.run(False)

# p = prev_wins.PREV_WINS(2566556, 10000, True);
# p.explore(False);
# p.print_summary()
#############################
# fg = FillGaps();
# # # #fg.generate();
# fg.generate_hotspot();
#fg.generate_keno();


#######REPORT##########
# r = ireport.iReport();
# r.save();

# r = depth_summary.DepthSummary();
# print(r.get_file())
# r.get_dataframe()
# r.data_query();
# r.run();

# de = data_export.DataExport();
# de.run();

# vr = db_validation_report.DBValidationReport();
# vr.run();

# dr = idraw.iDraw(2277311);
# # draws = dr.db.session.query(idraw.iDraw).order_by(idraw.iDraw.draw_id.asc()).all()
# # for draw in draws:
# #     draw.setBin();
# dr.setBinBySQL();


##################
# import pandas as pd
# import xlsxwriter
# from utils import Utils



# dr = idraw.iDraw();
# query = dr.db.session.query(idraw.iDraw).filter(idraw.iDraw.draw_id > 2566550);
# # results = query.all();
# # print(results)

# df = pd.read_sql(query.statement, dr.db.session.bind);

# #location = r'Y:/rancheros/eclipse/instance/data/workspaces/workspace4i8ynyxq64yvcgk8/medikid-PyLotto/data/reports/df.xlsx'
# location = 'data/reports/df1.xlsx'

# xlsx = pd.ExcelWriter(location, engine='xlsxwriter');

# xl = df.to_excel(xlsx, sheet_name='data', index=None, header=True)
# print(df)

# xlsx.save();
# print(Utils.getTimeStamp())




##################

#dr = idraw.iDraw();
#print(dr.get_min('draw_id'));

#//replaced on 1268 pymysql/connection.py
#self.server_charset = charset_by_id(lang).name
            #//// replaced to fix KEY ERROR 255
            #try:
                #self.server_charset = charset_by_id(lang).name
            #except KeyError:
                #self.server_charset = None
            #/////
#/replaced line 1569 sqlalchemy/dialetcts/base.py
#('SELECT @@tx_isolation') #replaced tx_isolation with transaction_isolation


# ball = iball.iBall(1);
# ball.set_score("Overall", 0.3);
# ball.set_score("depth", 0.457)
# print(ball.toString())




# pr = ipreds.iPreds(201938337);
# pr.set_pred(1,0.1)
# pr.set_pred(2,0.2)
# pr.db_save()

# print(pr.get_pred(1))

# ses = Session("hotspot");
# ses.run("rand_01_001", 2277330, 10, 10, True);
#ses.validateTickets(2277330)
# ticket = iticket.iTicket(2277339);
# ticket.validate();

# bowl = ibowl.iBowl(80);
# bowl.setScore(1, "num", 0.123);
# bowl.setScore(8, "num", 1.1)
# bowl.setScore(5, "num", 0.9)
# bowl.setScore(35,"num", 1.3)
# bowl.setScore(70, "num", 1.0)

# bowl.setScore(3, "overall", 1.2)
# bowl.setScore(7, "overall", 0.5)

# nums = bowl.getArrayNums();
# a_score_nums = bowl.getArrayScores("num");
# #a_score_overall = bowl.getArrayScores("overall")
# print(nums)
# print(a_score_nums)
# #print(a_score_overall)
# print(bowl.pickRand(10))
# print(bowl.pickWeightedRand(10, "num", True))

# dr = idraw.iDraw(2277330);
# dr.setup();
# dr.setBin();
# dr.db_update({'d_bin0140':dr.d_bin0140, 'd_bin4180': dr.d_bin4180}, {'draw_id':2277311})
# print(dr.d_bin0140, " ", dr.d_bin4180)
