from hotspot.models import iresult,idraw, idepth, ireport, ibin
import pandas as pd


class DBValidationReport(ireport.iReport):
    _FILE_NAME = 'DBValidationReport'
          
    _DF_REPORT = None
    _DF_RESULTS = None
    _DF_DRAWS = None
    _DF_DEPTHS = None

    def __init__(self):
        super().__init__(self._FILE_NAME);
    
    def data_query(self):
        query = self.db.session.query(idepth.iDepth).filter(idepth.iDepth.draw_id > 2566550);
        return query;
        #results = query.execute();

    def process_dataframe(self):
        df = self._DF;
        print(df['draw_id'])
        for index, row in df.iterrows():
            print(row['draw_id'])
        return self._DF;

    def find_gaps(self, TableName='results', FixIt=False):
        DF = pd.DataFrame();

        if ( TableName == 'results'):
            DF = self._DF_RESULTS;
        elif (TableName == 'draws'):
            DF = self._DF_DRAWS;
        elif (TableName == 'depths'):
            DF = self._DF_DEPTHS;

        prev_draw_id = DF['draw_id'].min() - 1;
        print("Finding gaps in %s" % TableName);
        print("Starting from draw id %i" % prev_draw_id)

        for index, row in DF.iterrows():
            if ( (row['draw_id'] - prev_draw_id) > 1):
                print("Missing draw from %i to %i" % (prev_draw_id, row['draw_id']))
                self._DF = self._DF.append({ #df.append does not work in place
                    'Error' : 'GAP',
                    'Table' : TableName,
                    'DrawID': row['draw_id'],
                    'Key' : 'draw_id',
                    'Value' : row['draw_id'],
                    'Actual' : prev_draw_id + 1,
                    'Fixed' : ''
                    }, ignore_index=True)
            prev_draw_id = row['draw_id'];
        
    def find_empty_bins(self, fix_it = False):
        #DF = self._DF_DRAWS[ self._DF_DRAWS.d_bin0140.isnull() | self._DF_DRAWS.d_bin4180.isnull() ];
        DF = self._DF_DRAWS.filter( self._DF_DRAWS.d_bin0140.isnull() | self._DF_DRAWS.d_bin4180.isnull() , axis = 0);
        print("Found %i draws with issing binary fields" % len(DF) )
        # for index, row in DF.iterrows():
        #     self._DF = self._DF.append({ #df.append does not work in place
        #             'Error' : 'EMPTY_BIN',
        #             'Table' : 'draws',
        #             'DrawID': row['draw_id'],
        #             'Key' : 'd_bin0140',
        #             'Value' : '',
        #             'Actual' : '',
        #             'Fixed' : ''
        #             }, ignore_index=True);


    def validate_depths(self):
        for index, row in self._DF_DEPTHS.iterrows():
            i =1; b0140 = ibin.iBin(); b4180 = ibin.iBin();
            while (i <= 40):
                key = 'n'+str(i); val = int(row[key]); prev_val = self._DF_DEPTHS.loc(self._DF_DEPTHS.index[index-1], key) #self._DF_DEPTHS[row['draw_id']-1][key]
                if (val == 0):
                    b0140.set_bit(i);
                else:
                    if (val - prev_val > 1):
                        self._DF = self._DF.append({ #df.append does not work in place
                            'Error' : 'DEPTH_MISMATCH',
                            'Table' : 'depths',
                            'DrawID': row['draw_id'],
                            'Key' : key,
                            'Value' : val,
                            'Actual' : prev_val + 1,
                            'Fixed' : ''
                        }, ignore_index=True);
                i += 1;

            
            while (i <= 80):
                key = 'n'+str(i); val = int(row[key]); prev_val = self._DF_DEPTHS.loc(self._DF_DEPTHS.index[index-1], key) #self._DF_DEPTHS[row['draw_id']-1][key]
              
                if (val == 0):
                    b4180.set_bit(i);
                else:
                    if ((val - prev_val) > 1):
                        self._DF = self._DF.append({ #df.append does not work in place
                            'Error' : 'DEPTH_MISMATCH',
                            'Table' : 'depths',
                            'DrawID': row['draw_id'],
                            'Key' : 'n'+str(i),
                            'Value' : val,
                            'Actual' : prev_val + 1,
                            'Fixed' : ''
                        }, ignore_index=True);

                i += 1;

        if (self._DF_REPORT[row['draw_id']].d_bin0140 == b0140.get_bin() or self._DF_REPORT[row['draw_id']].d_bin0140 == b4180.get_bin()):
            self._DF = self._DF.append({ #df.append does not work in place
                            'Error' : 'BIN_MISMATCH',
                            'Table' : 'draws',
                            'DrawID': row['draw_id'],
                            'Key' : 'n'+str(i),
                            'Value' : row['n'+str(i)] ,
                            'Actual' : '' ,#self._DF_DEPTHS[row['draw_id']-1]['n'+str(i)] + 1,
                            'Fixed' : ''
                        }, ignore_index=True);
            

        
        
        



    def run(self):
        self._DF = pd.DataFrame(columns=['Error', 'Table','DrawID', 'Key', 'Value', 'Actual', 'Fixed'])
        #self._DF_RESULTS = iresult.iResult().get_dataframe();
        self._DF_DRAWS = idraw.iDraw().get_dataframe();
        #self._DF_DEPTHS = idepth.iDepth().get_dataframe();

        #check for gaps
        # self.find_gaps('results');
        # self.find_gaps('draws');
        # self.find_gaps('depths');

        #find empty d_bins
        self.find_empty_bins();

        #results vs draws


        #draws vs depths

        self.write_dataframe(self._DF, 'ValReport');
        print(self._DF)
        self._WRITER.save()