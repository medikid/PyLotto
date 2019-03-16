'''
Created on Dec 22, 2017

@author: somaj
'''

from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean
from sqlalchemy import select, delete, update, insert, exc
from sqlalchemy.ext.declarative import declarative_base

from powerball.db import db_init;
from powerball.models import Base

from datetime import datetime
from utils import Utils;
#from MySQLdb.constants.FLAG import AUTO_INCREMENT

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
            self.db_get_or_create()
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
        result = self.db.session.query(self.__className).filter(filter_statement , addl_filter_statement)
        #result = query.filter(addl_filter_statement)
        #print('Filter Statement', filter_statement)
        
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
        print(query)
        instance = query.first();
        
        if instance:
            print('Object already exists')
            return instance
        else:
            self.db.session.add(self)
            self.db.session.commit()
            print('Object saved')
            return self
        
    