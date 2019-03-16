
from keno.models import iresult, idraw, idepth;
from keno.fetcher import Fetcher
from keno.db import db_init;
from keno.db.db_base import DBBase

import numpy as np

class Keno:
    db=db_init()
    
    def get_last_draw_id(self):
        res = iresult.iResult()
        return res.getLastDrawID()
    
    def derive(self, from_id, to_id):
        result_id = from_id;     
        while(result_id <= to_id):
            new_draw=idraw.iDraw(result_id)
            new_draw.derive()
            new_draw.db_save()
                #new_draw.toString()
                  
            new_depth=idepth.iDepth(result_id);
            new_depth.derive();
            new_depth.db_save()
            #new_depth.toString()
            result_id += 1;
    
    
    def sync(self):
        last_draw_id = self.get_last_draw_id();
        #last_draw_id=307657;
        next_draw_id = last_draw_id + 1;
        f = Fetcher();
        while(True):
            print("Syncing "+str(next_draw_id))
            new_res = f.fetch_result(next_draw_id)
            print(new_res.toString())
            new_res.db_save()
            
            new_draw=idraw.iDraw(next_draw_id)
            new_draw.derive()
            new_draw.db_save()
            #new_draw.toString()
              
            new_depth=idepth.iDepth(next_draw_id);
            new_depth.derive();
            new_depth.db_save()
            #new_depth.toString()          
             
            next_draw_id += 1;
            
    
    def get_all_results(self):            
        master_dict = {}
        results = self.db.session.query(iresult.iResult).order_by(iresult.iResult.draw_id.asc()).all()
        for result in results:
            master_dict.update(result.get_dict())
            
        return master_dict;
            
    def get_all_draws(self):
        master_dict = {}
        draws = self.db.session.query(idraw.iDraw).order_by(idraw.iDraw.draw_id.asc()).all()
        for draw in draws:
            master_dict.update(draw.get_dict())
            
        return master_dict;
    
    def get_all_depths(self):
        master_dict = {}
        depths = self.db.session.query(idepth.iDepth).order_by(idepth.iDepth.draw_id.asc()).all()
        for depth in depths:
            master_dict.update(depth.get_dict())
            
        return master_dict;
    
    def validate_db(self):
        val_obs = {'missing':[],'invalid':[]};
        
        draw_ids_results = []
        first_draw = 1;
        last_draw = 345678;
        
        val_obs['missing']['results'] = sorted(set(range(first_draw, last_draw)).difference(draw_ids_results))
        
        master_results_d = self.get_all_results();
        master_draws_d = self.get_all_draws();
        master_depths_d = self.get_all_depths();
        
                
        master_draws_a = [];
        for key, value in master_draws_d.items():
            master_draws_a.append(value)
        
        master_draws = np.matrix(master_draws_a)
        print(master_draws.shape)
        
        
        np.savez('master_draws', master_draws)
#         np.savez('master_draws', master_draws.values())
#         np.savez('master_depths', master_depths.values())
#         
#         first_draw_id = self.db.session.query(iresult.iResult).order_by(iresult.iResult.draw_id.asc()).first().draw_id;
#         last_draw_id = self.db.session.query(iresult.iResult).order_by(iresult.iResult.draw_id.asc()).first().draw_id;
#         next_draw_id = first_draw_id + 1;
#         
#         while (next_draw_id < last_draw_id):
#             print(master_results[next_draw_id])
#             print(master_draws[next_draw_id])
#             print(master_depths[next_draw_id])
#             
#             next_draw_id +=1;
#         
#         next_draw_id = first_draw_id + 1;
#         while (next_draw_id < last_draw_id):
#             if next_draw_id not in master_results:  val_obs['missing']['results']= next_draw_id; 
#             if next_draw_id not in master_draws:  val_obs['missing']['draws']= next_draw_id; 
#             if next_draw_id in master_depths:  val_obs['missing']['depths']= next_draw_id; 
#             
#             next_draw_id +=1;
#             
        
        
        return val_obs;
    
    def save_master_matrix(self):
        data_folder='strategies/data/keno/'
        master_results_d = self.get_all_results();
        master_draws_d = self.get_all_draws();
        master_depths_d = self.get_all_depths();
        
        master_results_a = []        
        master_draws_a = [];
        master_depths_a=[]
        master_ids_a=[]
        
        for key, value in master_draws_d.items():
            master_ids_a.append(np.array([key]))
            master_draws_a.append(value)
            master_results_a.append(master_results_d.get(key))
            
        for key, value in master_depths_d.items():
            master_depths_a.append(value)    
        
            
        master_ids = np.matrix(master_ids_a)
        master_results = np.matrix(master_results_a)
        master_draws = np.matrix(master_draws_a).astype(float)
        master_depths = np.matrix(master_depths_a).astype(float)
        
        np.savez(data_folder+'data_245M', ids=master_ids, results=master_results, draws=master_draws, depths=master_depths)       
        np.savez(data_folder+'master_ids_245M', ids=master_ids)
        np.savez(data_folder+'master_results_245M', results=master_results)
        np.savez(data_folder+'master_draws_245M', draws=master_draws.astype(float))
        np.savez(data_folder+'master_depths_245M', depths=master_depths.astype(float))
        
        np.savez(data_folder+'train_2M', ids=master_ids[0:2000000], train=master_depths[0:2000000], target=master_draws[1:2000001]);
        np.savez(data_folder+'val_2M', ids=master_ids[2000000:2001000], val=master_depths[2000000:2001000], target=master_draws[2000001:2001001]);
        np.savez(data_folder+'test_2M', ids=master_ids[2001000:2002000], test=master_depths[2001000:2002000], target=master_draws[2001001:2002001]);
        
        
        np.savez(data_folder+'train_1M', ids=master_ids[0:1000000], train=master_depths[0:1000000], target=master_draws[1:1000001]);
        np.savez(data_folder+'val_1M', ids=master_ids[1000000:1001000], val=master_depths[1000000:1001000], target=master_draws[1000001:1001001]);
        np.savez(data_folder+'test_1M', ids=master_ids[1001000:1002000], test=master_depths[1001000:1002000], target=master_draws[1001001:1002001]);
        
        np.savez(data_folder+'train_1-2M', ids=master_ids[1000000:2000000], train=master_depths[1000000:2000000], target=master_draws[1000001:20010001]);
        np.savez(data_folder+'val_1-2M', ids=master_ids[2000000:2001000], val=master_depths[2000000:2001000], target=master_draws[2000001:2001001]);
        np.savez(data_folder+'test_1-2M', ids=master_ids[2001000:2002000], test=master_depths[2001000:2002000], target=master_draws[2001001:2002001]);
        
        np.savez(data_folder+'train_2-245M', ids=master_ids[2000000:2245000], train=master_depths[2000000:2245000], target=master_draws[2000000:2245000]);
        np.savez(data_folder+'val_2-245M', ids=master_ids[2245000:2246000], val=master_depths[2245000:2246000], target=master_draws[2245001:2246001]);
        np.savez(data_folder+'test_2-245M', ids=master_ids[2246000:2247000], test=master_depths[2246000:2247000], target=master_draws[2246001:2247001]);
           
k = Keno();
#k.derive(2247068)
#k.save_master_matrix()
#print(h.save_master_matrix())