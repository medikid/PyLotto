from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean, BigInteger
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from keno.db import db_init;
from keno.db.db_base import DBBase
from keno.models import Base, ipick, iresult

import numpy as np

class iDraw(Base, DBBase):
    __tablename__ = 'draws'    
    __table_args__ = {'extend_existing': True}
    db = db_init();
    
    draw_id=Column(Integer,primary_key=True, autoincrement=False)
    n1=Column(Integer)
    n2=Column(Integer)
    n3=Column(Integer)
    n4=Column(Integer)
    n5=Column(Integer)
    n6=Column(Integer)
    n7=Column(Integer)
    n8=Column(Integer)
    n9=Column(Integer)
    n10=Column(Integer)
    n11=Column(Integer)
    n12=Column(Integer)
    n13=Column(Integer)
    n14=Column(Integer)
    n15=Column(Integer)
    n16=Column(Integer)
    n17=Column(Integer)
    n18=Column(Integer)
    n19=Column(Integer)
    n20=Column(Integer)
    n21=Column(Integer)
    n22=Column(Integer)
    n23=Column(Integer)
    n24=Column(Integer)
    n25=Column(Integer)
    n26=Column(Integer)
    n27=Column(Integer)
    n28=Column(Integer)
    n29=Column(Integer)
    n30=Column(Integer)
    n31=Column(Integer)
    n32=Column(Integer)
    n33=Column(Integer)
    n34=Column(Integer)
    n35=Column(Integer)
    n36=Column(Integer)
    n37=Column(Integer)
    n38=Column(Integer)
    n39=Column(Integer)
    n40=Column(Integer)
    n41=Column(Integer)
    n42=Column(Integer)
    n43=Column(Integer)
    n44=Column(Integer)
    n45=Column(Integer)
    n46=Column(Integer)
    n47=Column(Integer)
    n48=Column(Integer)
    n49=Column(Integer)
    n50=Column(Integer)
    n51=Column(Integer)
    n52=Column(Integer)
    n53=Column(Integer)
    n54=Column(Integer)
    n55=Column(Integer)
    n56=Column(Integer)
    n57=Column(Integer)
    n58=Column(Integer)
    n59=Column(Integer)
    n60=Column(Integer)
    n61=Column(Integer)
    n62=Column(Integer)
    n63=Column(Integer)
    n64=Column(Integer)
    n65=Column(Integer)
    n66=Column(Integer)
    n67=Column(Integer)
    n68=Column(Integer)
    n69=Column(Integer)
    n70=Column(Integer)
    n71=Column(Integer)
    n72=Column(Integer)
    n73=Column(Integer)
    n74=Column(Integer)
    n75=Column(Integer)
    n76=Column(Integer)
    n77=Column(Integer)
    n78=Column(Integer)
    n79=Column(Integer)
    n80=Column(Integer)
    mega=Column(Integer)
    d_bin0140=Column(BigInteger)
    d_bin4180=Column(BigInteger)
    
    drawDict={0:0}
    
    def __init__(self, DrawID=0):        
        self.reset()
        self.draw_id=DrawID
        if (self.draw_id>0): self.setup()
        
        super().setupDBBase(iDraw, iDraw.draw_id, self.draw_id)
        
    def reset(self):        
        for i in range(81):            
            self.drawDict[i]=0;
            if i>0:
                setattr(self, "n"+str(i), 0);
        self.mega = 0;
        self.d_bin0140 = 0;
        self.d_bin4180 = 0;
                
    def derive(self):
        if (self.draw_id>0):
            self.reset()
            
            #remove bin setting as it is resource intensive. We will use SQL
            #b0140 = ibin.iBin();
            #b4180 = ibin.iBin();

            r = iresult.iResult(self.draw_id);
            r.setup(); #setup from db
            self.mega=r.mega
            for x in r.pick.getArray():
                setattr(self,"n"+str(x),1)
                self.drawDict[x]=1
                
                #if x > 40:
            #         posn = x - 40;
            #         b4180.set_bit(posn);
            #     else: b0140.set_bit(x)
            

            # self.d_bin0140 = b0140.get_bin(); #770947678208
            # self.d_bin4180 = b4180.get_bin();  #8606711840

    def setBin(self):
        i =1; b0140 = ibin.iBin(); b4180 = ibin.iBin();
        while (i <= 80):
            dr = getattr(self,"n"+str(i))
            if dr == 1:
                if i > 40:
                    b4180.set_bit(i)
                else: b0140.set_bit(i)
            i += 1;
        self.d_bin0140 = b0140.get_bin(); #833831981626 for 2277311
        self.d_bin4180 = b4180.get_bin();  #206435647488 for 2277311

        #update db

        d = self.db.session.query(iDraw).filter(iDraw.draw_id==self.draw_id).update({iDraw.d_bin0140:self.d_bin0140, iDraw.d_bin4180:self.d_bin4180}, synchronize_session='fetch')
        self.db.session.commit()
    
    def setBinBySQL(self):
        #single draw_id
        # sql_statement = text(""" UPDATE `draws` SET `d_bin0140`=CONV(CONCAT(`n1`, `n2`, `n3`, `n4`, `n5`, `n6`, `n7`, `n8`, `n9`, `n10`, `n11`, `n12`, `n13`, `n14`, `n15`, `n16`, `n17`, `n18`, `n19`, `n20`, `n21`, `n22`, `n23`, `n24`, `n25`, `n26`, `n27`, `n28`, `n29`, `n30`, `n31`, `n32`, `n33`, `n34`, `n35`, `n36`, `n37`, `n38`, `n39`, `n40`),2,10), `d_bin4180`=CONV(CONCAT(`n41`, `n42`, `n43`, `n44`, `n45`, `n46`, `n47`, `n48`, `n49`, `n50`, `n51`, `n52`, `n53`, `n54`, `n55`, `n56`, `n57`, `n58`, `n59`, `n60`, `n61`, `n62`, `n63`, `n64`, `n65`, `n66`, `n67`, `n68`, `n69`, `n70`, `n71`, `n72`, `n73`, `n74`, `n75`, `n76`, `n77`, `n78`, `n79`, `n80`),2,10) WHERE `draw_id` = :draw_id """);
        # self.db.session.execute(sql_statement,  { "draw_id": self.draw_id } )

        #multiple draw_ids with dbin value null or 0
        sql_statement = text(""" UPDATE `draws` SET `d_bin0140`=CONV(CONCAT(`n1`, `n2`, `n3`, `n4`, `n5`, `n6`, `n7`, `n8`, `n9`, `n10`, `n11`, `n12`, `n13`, `n14`, `n15`, `n16`, `n17`, `n18`, `n19`, `n20`, `n21`, `n22`, `n23`, `n24`, `n25`, `n26`, `n27`, `n28`, `n29`, `n30`, `n31`, `n32`, `n33`, `n34`, `n35`, `n36`, `n37`, `n38`, `n39`, `n40`),2,10), `d_bin4180`=CONV(CONCAT(`n41`, `n42`, `n43`, `n44`, `n45`, `n46`, `n47`, `n48`, `n49`, `n50`, `n51`, `n52`, `n53`, `n54`, `n55`, `n56`, `n57`, `n58`, `n59`, `n60`, `n61`, `n62`, `n63`, `n64`, `n65`, `n66`, `n67`, `n68`, `n69`, `n70`, `n71`, `n72`, `n73`, `n74`, `n75`, `n76`, `n77`, `n78`, `n79`, `n80`),2,10) WHERE `d_bin0140` IS NULL or `d_bin0140` = 0 or `d_bin4180` IS NULL or `d_bin4180` = 0 """);
        self.db.session.execute(sql_statement)
        
        
    def setup(self):
        d = self.db.session.query(iDraw).filter(iDraw.draw_id==self.draw_id).first();

        if d is not None:
            
            for i in self.drawDict.keys():
                if (i>0):
                    setattr(self, "n"+str(i), getattr(d,"n"+str(i)) )
                    self.drawDict[i]=getattr(self, "n"+str(i))
            self.mega=d.mega
            self.d_bin0140=d.d_bin0140
            self.d_bin4180=d.d_bin4180
        
    def toString(self):
        return str(self.get_dict())  + "[" + str(self.mega)+"]"
            
            
    def get_dict(self):
        dict={};
        dict[self.draw_id]=np.array([self.n1, self.n2, self.n3, self.n4, self.n5, self.n6, self.n7, self.n8, self.n9, self.n10, self.n11, self.n12, self.n13, self.n14, self.n15, self.n16, self.n17, self.n18, self.n19, self.n20, self.n21, self.n22, self.n23, self.n24, self.n25, self.n26, self.n27, self.n28, self.n29, self.n30, self.n31, self.n32, self.n33, self.n34, self.n35, self.n36, self.n37, self.n38, self.n39, self.n40, self.n41, self.n42, self.n43, self.n44, self.n45, self.n46, self.n47, self.n48, self.n49, self.n50, self.n51, self.n52, self.n53, self.n54, self.n55, self.n56, self.n57, self.n58, self.n59, self.n60, self.n61, self.n62, self.n63, self.n64, self.n65, self.n66, self.n67, self.n68, self.n69, self.n70, self.n71, self.n72, self.n73, self.n74, self.n75, self.n76, self.n77, self.n78, self.n79, self.n80, self.d_bin0140, self.d_bin4180])
        return dict;

    def __get_dict__(self):
        dic = {};
        dic[self.draw_id] = {};

        i = 1;
        while (i <=80):
            dic[self.draw_id][i] = getattr(self, "n"+str(i));
            i += 1;
        
        dic[self.draw_id]['d_bin0140'] = self.d_bin0140;
        dic[self.draw_id]['d_bin4180'] = self.d_bin4180;

        return dic;