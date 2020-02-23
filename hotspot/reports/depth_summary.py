from hotspot.models import iresult,idraw, idepth, ireport


class DepthSummary(ireport.iReport):
    _FILE_NAME = 'Depth_Summary'

    def __init__(self):
        super().__init__(self._FILE_NAME);

        pass;
    
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