'''
Created on Dec 22, 2017

@author: somaj
'''

from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean
from sqlalchemy import select, delete, update, insert, exc
from sqlalchemy import func, distinct
from sqlalchemy.ext.declarative import declarative_base

from hotspot.db import db_init;
from hotspot.models import Base

from datetime import datetime
from utils import Utils;
#from MySQLdb.constants.FLAG import AUTO_INCREMENT

import pandas as pd

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

from flask import request


class DBBase():
    __tableName=''
    __primaryKeyField=''
    __primaryKeyValue=''
    base=''
    db_engine=''
    extend_existing=True 
   
    def __init__(self):
        pass;
        
    def setupDBBase(self, className, PrimaryKeyField, PrimaryKeyValue):
        self.set_base(Base())
        self.set_db_engine(self.db.db_engine);
        self.set_tablename(self.__tablename__)
        
        ########### SET THIS UP FOR EACH CLASS #############
        self.set_classname(className)
        self.set_primarykeys(PrimaryKeyField, PrimaryKeyValue)

    def set_base(self, base):
        self.base=base;
        
    def set_db_engine(self, dbEngine):
        self.db_engine = dbEngine;
        
    def set_tablename(self, tableName):
        self.__tablename=tableName
        pass
        
    def get_tablename(self):
        return self.__tablename;
        pass
    
    def set_classname(self, className):
        self.__className = className;
    
    def get_classname(self):
        return self.__className;
    
    def set_primarykeys(self, primaryKeyField, primaryKeyValue):
        self.__primaryKeyField = primaryKeyField;
        self.__primaryKeyValue = primaryKeyValue
    
    def get_primarykeyField(self):
        return self.__primaryKeyField;
    
    def get_primaryKeyValue(self):
        return self.__primaryKeyValue
    
    def create_table(self):
        self.base.metadata.create_all(self.db_engine);
        pass
        
    def db_save(self):
        try:
            return self.db_get_or_create()
        except exc.IntegrityError as e:
            self.db.session.rollback()
#         self.db.session.add(self)
#         self.db.session.commit()
        
        
    def selectAll(self, isExchangeSpecific=False):
        if isExchangeSpecific == False:
            query = self.db.session.query(self.__className).all();
        else:
            filter_statement= self.__className.exchange_id == self.exchange_id;
            query = self.db.session.query(self.__className).filter(filter_statement).all();
        return query;
    
    def selectWhere(self, filterKey, filterValue, isExchangeSpecific=False):
#         filter_statement = filterKey + ' = \'' + filterValue + '\'';
#         if (isExchangeSpecific==True):            
#             filter_statement = " , " + 'exchange_id' + ' = \'' + self.exchange_id + '\'';
        #result=''   
        filter_statement=''
        if (isExchangeSpecific==True): 
            filter_statement += self.__className.exchange_id == self.exchange_id
            
        addl_filter_statement = filterKey == filterValue
        #print('addl_filter_statement', addl_filter_statement)
        #result = self.db.session.query(self.__className).filter(filter_statement , addl_filter_statement)
        
        result = self.db.session.query(self.__className).filter(addl_filter_statement)
        
        #result = query.filter(addl_filter_statement)
        
        
        return result;
    
    def selectWheres(self, filterKeys, filterOperators, filterValues, isExchangeSpecific=False):
        filter_statement = '';
        if (isExchangeSpecific==True): filter_statement += self.__className.exchange_id == self.exchange_id;
        for i in range(len(filterKeys)):
            if(i > 0):filter_statement += ',';
            filter_statement += filterKeys[i] + filterOperators[i] + filterValues[i];
        
        ### CONCATENATION OF FILTERSTATEMENT DOES NOT WORK, you
        query = self.db.session.query(self.__className).filter(filter_statement);
        #print(filterStatement);
        return query;
        
    def db_get_or_create(self):
        query = self.selectWhere(self.__primaryKeyField, self.__primaryKeyValue)
        #query = self.db.session.query(self.__className).filter(self.__primaryKeyField == self.__primaryKeyValue)
        #print(query)
        instance = query.first();
        
        if instance:
            print('Object already exists')
            return instance
        else:
            self.db.session.add(self)
            return self.db.session.commit()
            #print('Object saved')

    def db_update(self, update_key_values, filter_key_values, isExchangeSpecific=False):
        filter_statement = ''; update_statement=''
        if (isExchangeSpecific==True): filter_statement += self.__className.exchange_id == self.exchange_id;
        i=0;
        for k,v in filter_key_values.items():
            if(i > 0):filter_statement += ',';
            filter_statement += k + '=' + str(v);
            i+=1;
        

        z=0
        for x,y in update_key_values.items():
            if(z > 0):update_statement += ',';
            update_statement += x + '=' + str(y);
            z+=1;

        #print("Update: ", update_statement, " Filter By: ", filter_statement)

        query = self.db.session.query(self.__className).filter(filter_statement).update(update_key_values, synchronize_session='fetch');
        self.db.session.commit()

    def get_max(self, key):
        query = select([func.max(getattr(self.__className, key))])        
        max = self.db.session.execute(query).scalar();
        
        return max;

    def get_min(self, key):
        query = select([func.min(getattr(self.__className, key))])        
        min = self.db.session.execute(query).scalar();
              
        return min;

    def get_dataframe(self, filterKeys=None, filterOperators=None, filterValues=None, isExchangeSpecific=False):
        filter_statement = '';
        query = self.db.session.query(self.__className);

        if (isExchangeSpecific==True): filter_statement += self.__className.exchange_id == self.exchange_id;
        
        if (filterKeys == None):
            query = query;
        else:
            for i in range(len(filterKeys)):
                if(i > 0):filter_statement += ',';
                filter_statement += filterKeys[i] + filterOperators[i] + filterValues[i];
        
                ### CONCATENATION OF FILTERSTATEMENT DOES NOT WORK, you
            query = query.filter(filter_statement);
        query = query.order_by(self.__primaryKeyField.asc())
        print(filter_statement);
        df = pd.read_sql(query.statement, self.db.session.bind)
        #df = df.set_index(self.__primaryKeyField)
        return df;

    def upload_dataframe(self, df, upload_index=True):
        df.to_sql(name=self.__tablename, con=self.db.db_engine, if_exists='append', index=upload_index)
