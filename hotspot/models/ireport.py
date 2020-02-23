from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, Boolean, BigInteger
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Integer, DateTime
from wsgiref.handlers import format_date_time

from hotspot.db import db_init;
from hotspot.db.db_base import DBBase
from hotspot.models import Base, ipick, iresult, ibin, idraw
from utils import Utils

import numpy as np
import pandas as pd
import xlsxwriter
import os

class iReport:
    # https://www.dataquest.io/blog/excel-and-pandas/
    db = db_init();
    _FILE=None;
    _WORKBOOK = None;
    _WORKSHEET=None;
    _FILE_NAME = '';
    _FILE_FORMAT = 'xlsx'
    _FILE_LOCATION_R = '/data/reports/';
    _FILE_LOCATION = r'Y:/rancheros/eclipse/instance/data/workspaces/workspace4i8ynyxq64yvcgk8/medikid-PyLotto/data/reports/'
    _WRITER = None;
    _DF = None;
    headers = []
    rows = {}

    def __init__(self, FileName=None, FileFormat="xlsx"):
        self._FILE_FORMAT = FileFormat;
        
        if (FileName == None):
            print("File Name not set")
        else: 
            self._FILE_NAME = FileName
            self.set_writer()
            #self.file_open();

    def get_file_name(self):
        return Utils.getTimeStamp() + '_Hotspot_' + self._FILE_NAME + "." + self._FILE_FORMAT;
    
    def get_file(self):
        return self._FILE_LOCATION + self.get_file_name();
        return os.path.join(self._FILE_LOCATION, self.get_file_name())

    def set_writer(self):
        if (self._FILE_FORMAT=="csv"):
            self._WRITER = pd.DataFrame.to_csv(self.get_file())
        elif (self._FILE_FORMAT == "xlsx"):
            self._WRITER = pd.ExcelWriter(self.get_file(), engine='xlsxwriter')

    def set_workbook(self):
        self._WORKBOOK = self._WRITER.book
    
    def set_worksheet(self, SheetName='Data'):
        self._WORKSHEET = self._WRITER.sheets[SheetName];

    def write(self, SheetName=None):
        sn = ''
        if (SheetName == None):
            sn = self._FILE_NAME;
        else: sn = SheetName;
        
        if (self._FILE_FORMAT=="csv"):
            self._WRITER = self._DF.to_csv(self.get_file())
        elif (self._FILE_FORMAT == "xlsx"):            
            self._DF.to_excel(self._WRITER, sheet_name = sn);

    def write_dataframe(self, DF=None, SheetName='Data'):
        if (DF is not None):
            try:
                DF.to_excel(self._WRITER, index=None, sheet_name=SheetName)
            except:
                print("Could not write dataframe")

    
    def data_query(self):
        results = [];
        print("Not Implemented")
        return results;

    
    def process_dataframe(self):
        return self._DF;
    
    def get_dataframe(self):
        query = self.data_query();
        self._DF = pd.read_sql(query.statement, self.db.session.bind)
        self._DF = self.process_dataframe();
        return self._DF;

    def add_format(self):
        self.set_workbook();
        self.set_worksheet();


    def set_header_bold(self):
        header_fmt = self._WORKBOOK.add_format({'bold': True})
        self._WORKSHEET.set_row(0, None, header_fmt)


    def file_open(self):
        try:            
            self.set_writer()
            print("Opened file", self._FILE_NAME)
            
        except FileNotFoundError:
            print("File does not exist")
        except:
            print("Other error")

    def run(self):
        self.file_open();
        self.data_query();
        self.process_dataframe();
        self.write();
        self.set_header_bold();
        self.file_close()


    def file_close(self):
        self._WRITER.save();