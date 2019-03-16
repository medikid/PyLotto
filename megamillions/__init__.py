
from megamillions.models import iresult, idraw, idepth, ifreq;
from megamillions.fetcher import Fetcher
from megamillions.db import db_init;
from megamillions.db.db_base import DBBase

import numpy as np

class MegaMillions:
    db=db_init()
    
    def get_last_draw_id(self):
        res = iresult.iResult()
        return res.getLastDrawID()
    
    def sync(self):
        last_draw_id = 1380 #self.get_last_draw_id();
        latest = 1390
        next_draw_id = last_draw_id + 1;
        
        f = Fetcher();
        while(next_draw_id <= latest):
            print("Syncing "+str(next_draw_id))
            #new_res = f.fetch_result(next_draw_id)
            #print(new_res.toString())
            #new_res.db_save()
            
            new_draw=idraw.iDraw(next_draw_id)
            new_draw.derive()
            new_draw.db_save()
            new_draw.toString()
              
            new_depth=idepth.iDepth(next_draw_id);
            new_depth.derive();
            new_depth.db_save()
            new_depth.toString()          
             
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
    
    def derive_freqs(self, sample_size):
        last_draw_id =  self.get_last_draw_id()
        d_id_to_start = last_draw_id - sample_size;
        #freq_file = self.csv_file="E:/Projects/Lotto/megamillions/Results/freqs.csv"
        a_freqs = []        
        dict_depths = self.get_all_depths();
        n=0;freqs={0:0};
        while(n<75):
            d_id=d_id_to_start; last_value = 0;
            while d_id <= last_draw_id:
                #print(d_id, dict_depths.get(d_id)[n])
                if(dict_depths.get(d_id)[n]==0):
                    a_freqs.append(last_value)
                else: 
                    last_value = dict_depths.get(d_id)[n]
                 
                d_id+=1
            freqs[n] = a_freqs;
            a_freqs = []
            n+=1;
        print(freqs)
#         for depth in dict_depths:
#             print(depth.toString())
#         with open(freq_file, 'w') as f:
#             for k, v in freqs.items():
#                 f.write("%s," % k)
#                 for elem in v:
#                     f.write(str(elem))
#                 f.write("\n")
#             f.close()
        rows=52; #including score 0 and 51
        columns=75;
        fqs = np.zeros((rows,columns), dtype=int)
        for k, v in freqs.items():
            for elem in v:
                if elem <= 50:
                    fqs[elem][k] +=1
                else: fqs[51][k] +=1
        print(fqs)
         
         
         
        score=0;
        while score < 52:
            fq = ifreq.iFreq();
            fq.freq_id=None
            fq.draw_id = last_draw_id;
            fq.freq_sample = sample_size
            fq.freq_score = score;
            i=1
            while i < 75:
                #for i in range(columns):
                fq.set_key_value(i+1, int(fqs[score][i]))
                i+=1
                 
            fq.db_save()
            score +=1;
        
                
        
    
    def validate_db(self):
        val_obs = {'missing':[],'invalid':[]};
        
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
        data_folder='strategies/data/'
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
        
        np.savez(data_folder+'data', ids=master_ids, results=master_results, draws=master_draws, depths=master_depths)       
        np.savez(data_folder+'master_ids', ids=master_ids)
        np.savez(data_folder+'master_results', results=master_results)
        np.savez(data_folder+'master_draws', draws=master_draws.astype(float))
        np.savez(data_folder+'master_depths', depths=master_depths.astype(float))
        
        np.savez(data_folder+'train_75k', ids=master_ids[0:75000], train=master_depths[0:75000], target=master_draws[1:75001]);
        np.savez(data_folder+'val_75k', ids=master_ids[75000:77000], val=master_depths[75000:77000], target=master_draws[75001:77001]);
        np.savez(data_folder+'test_75k', ids=master_ids[77000:], test=master_depths[77000:-1], target=master_draws[77001:]);
        
        
        np.savez(data_folder+'train_1', ids=master_ids[0:10000], train=master_depths[0:10000], target=master_draws[1:10001]);
        np.savez(data_folder+'val_1', ids=master_ids[10000:11000], val=master_depths[10000:11000], target=master_draws[10001:11001]);
        np.savez(data_folder+'test_1', ids=master_ids[11000:12000], test=master_depths[11000:12000], target=master_draws[11001:12001]);
        
        np.savez(data_folder+'train_2', ids=master_ids[12000:22000], train=master_depths[12000:22000], target=master_draws[12001:22001]);
        np.savez(data_folder+'val_2', ids=master_ids[22000:23000], val=master_depths[22000:23000], target=master_draws[22001:23001]);
        np.savez(data_folder+'test_2', ids=master_ids[23000:24000], test=master_depths[23000:24000], target=master_draws[23001:24001]);
        
        np.savez(data_folder+'train_3', ids=master_ids[24000:34000], train=master_depths[24000:34000], target=master_draws[24001:34001]);
        np.savez(data_folder+'val_3', ids=master_ids[34000:35000], val=master_depths[34000:35000], target=master_draws[34001:35001]);
        np.savez(data_folder+'test_3', ids=master_ids[35000:36000], test=master_depths[35000:36000], target=master_draws[35001:36001]);
           
h = MegaMillions();
h.derive_freqs(50)
#print(h.get_last_draw_id())