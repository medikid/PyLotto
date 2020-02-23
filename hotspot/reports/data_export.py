from hotspot.models import iresult,idraw, idepth, ireport
import pandas as pd


class DataExport(ireport.iReport):
    _FILE_NAME = 'DataExport'
          

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

    def run(self):
        #r = iresult.iResult()
        #df_r = r.get_dataframe()
        #self.write_dataframe(df_r, 'Results');

        # dr = idraw.iDraw()
        # df_dr = dr.get_dataframe()
        # self.write_dataframe(df_dr, 'Draws');

        dp = idepth.iDepth()
        df_dp = dp.get_dataframe()
        self.write_dataframe(df_dp, 'Depths');

        self._WRITER.save()