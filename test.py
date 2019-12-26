from hotspot import HotSpot, fetcher;
from hotspot.models import iticket, iprize, isession, iball, ibowl, istrategy, ipreds, idraw
from hotspot.controllers import prizes
import os, ssl

from numpy.random import choice as np_choice
from random import choices as r_choices

from session import Session


h = HotSpot();
# print("Finding gaps ....")
h.find_gaps_results(1,2493350)
h.find_gaps_draws(1,2493350)
h.find_gaps_depths(1,2493350)


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