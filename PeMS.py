'''
Created on Feb 21, 2017

@author: Administrator
'''

import requests
from bs4 import BeautifulSoup
import time
import datetime

class PeMS:   
    def __init__(self):
        self.url = 'http://pems.dot.ca.gov/'
        
    def initSession(self):
        session = requests.session()
        values = {'username' : 'bumsubp@uci.edu',
                  'password':'javawm',
                  'submit':'login',}
        r=session.post(self.url, data=values)
        return r, session
    
class ChangeLog:
    def __init__(self, session, id):
        self.id =id
        self.url = "http://pems.dot.ca.gov/?html_x=48&report_form=1&pagenum_all=1&county_id=59&station_id="+self.id+"&dnode=VDS"        
        r=session.get(self.url)
        soup = BeautifulSoup(r.content,"lxml")
        self.cl = soup.findAll('table', attrs={"class": "blue_outline_table"})
        self.sd = soup.findAll('div', attrs={"class": "segmentPanelSection"})
        self.attrs = {
                      0: [None,  'Station ID',                      0],
                      ## Roadway Information (from TSN)
                      1: [None,  'Road Width',                      1],
                      2: [None,  'Lane Width',                      2],
                      3: [None,  'Inner Shoulder Width',            3],
                      4: [None,  'Inner Shoulder Treated Width',    4],
                      5: [None,  'Outer Shoulder Width',            5],
                      6: [None,  'Outer Shoulder Treated Width',    6],
                      7: [None,  'Design Speed Limit',              7],
                      8: [None,  'Functional Class',                8],
                      9: [None,  'Inner Median Type',               9],
                      10:[None,  'Inner Median Width',             10],
                      11:[None,  'Terrain',                         11],
                      12:[None,  'Population',                      12],
                      13:[None,  'Barrier',                         13],
                      14:[None,  'Surface',                         14],
                      15:[None,  'Roadway Use',                     15],
                      ## Change Log
                      16: [None,  'Date',                           16],
                      17: [None,  'Status',                         17],
                      18: [None,  'Name',                           18],
                      19: [None,  'Lanes',                          19],
                      20: [None,  'CA PM',                          20],
                      21: [None,  'Abs PM',                         21],
                      22: [None,  'Length',                         22],
                      23: [None,  'Lat',                            23],
                      24: [None,  'Lng',                            24],
                      ## Staion Details
                      25: [None,  'Aliases',                        25],
                      26: [None,  'LDS',                            26],
                      27: [None,  'Owner',                          27],
                      28: [None,  'Assoc. Traffic Census Station',  28],
                      29: [None,  'Comm Type (LDS)',                29],
                      30: [None,  'Speeds',                         30],
                      31: [None,  'Max Cap.',                       31],
                      32: [None,  'Vehicle Classification',         32],
                      ## Lane Detection
                      33: [None,  'Lane',                           33],
                      34: [None,  'Slot',                           34],
                      35: [None,  'Sensor Tech',                    35],
                      36: [None,  'Type',                           36],
                      ## Diagnostics
                      37: [None,  'Threshold Set',                  37],
                      38: [None,  'Flow = 0, Occ > 0 (Intermittent)',38],
                      39: [None,  'High Flow Threshold',            39],
                      40: [None,  'High Occ Threshold',             40],
                      41: [None,  'High Occupancy (High Val)',      41],
                      42: [None,  'Occ = 0; Flow > 0 (Intermittent)',42],
                      43: [None,  'Repeat Occupancy (Constant)',    43],
                      44: [None,  'Occupancy = 0 (Card Off)',       44]
                      }
        
        self.station_ID()
        self.roadway_Information()
        self.change_Log()
        self.stationDetails()
        self.laneDetection()
        self.diagnostics()
        
    def __getitem__(self, key):
        if key in self.attrs:
            return self.attrs[key][0]
        
    def __setitem__(self, key, item):
        if key in self.attrs:
            self.attrs[key][0] = item
            
    def station_ID(self):
        self.attrs[0][0] = str(self.id)
        
    def roadway_Information(self):
        table1 = self.cl[0]
        tds = table1.findAll('td')
        for ind, td in enumerate(tds[1:]):
            if ind%2 == 1:
                self.attrs[(ind//2)+1][0] = str(td.getText())
    
    def change_Log(self):
        table2 = self.cl[1]
        trs = table2.findAll('tr')
        tds = trs[-1].findAll('td')
        for ind, td in enumerate(tds):
            self.attrs[ind+16][0] = str(td.getText())
    
    def stationDetails(self):
        table3 = self.sd[1]
        tds = table3.findAll('td')
        for ind, td in enumerate(tds):
            if ind%2 == 1:
                self.attrs[(ind//2)+25][0] = str(td.getText())
                
    def laneDetection(self):
        table4 = self.sd[2]
        trs = trs = table4.findAll('tr')
        tds = trs[1].findAll('td')
        for ind, td in enumerate(tds):
            self.attrs[ind+33][0] = str(td.getText())

    def diagnostics(self):
        table5 = self.sd[3]
        tds = table5.findAll('td')
        for ind, td in enumerate(tds):
            if ind%2 == 1:
                self.attrs[(ind//2)+37][0] = str(td.getText())

class Performance:
    def __init__(self, session, id):
        self.id = str(id)
        sDate = datetime.date(2014, 1, 1)
        eDate = datetime.date(2016, 12, 31)
        sUnixtime = str(int(time.mktime(sDate.timetuple())))
        eUnixtime = str(int(time.mktime(eDate.timetuple())))

                
        self.urlAADT = "http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=analysis&tab=aadt&export=&station_id="+self.id+"&s_time_id="+sUnixtime+"&e_time_id="+eUnixtime+"&html.x=46&html.y=14"
        self.urlDoW = "http://pems.dot.ca.gov/?s_time_id=1451635200&e_time_id=1483171200&html_x=33&report_form=1&tod=all&tod_from=0&tod_to=0&dnode=VDS&content=loops&tab=det_dow&station_id=1209746"
        r=session.get(self.urlAADT)
        soup = BeautifulSoup(r.content,"lxml")
        self.aa = soup.findAll('table', attrs={"class": "inlayTable"})
        
        self.attrs = {
                      0: [None,  'Incident',                    0],
                      ## AADT
                      1: [None,  'Starting Month',              1],
                      2: [None,  'Fwy',                         2],
                      3: [None,  'CA PM',                       3],
                      4: [None,  'Abs PM',                      4],
                      5: [None,  'VDS',                         5],
                      6: [None,  'Name',                        6],
                      7: [None,  'Type',                        7],
                      8: [None,  'Arithmetic Mean',             8],
                      9: [None,  'ASTM Std',                    9],
                      10:[None,  'Conv. AASHTO',                10],
                      11:[None,  'Prov. AASHTO',                11],
                      12:[None,  'Sum of 24 Annual Avg Hours',  12],
                      13:[None,  'Mod. ASTM Std',               13],
                      14:[None,  'Mod. Conv. AASHTO',           14],
                      15:[None,  'Mod. Prov. AASHTO',           15],
                      16:[None,  '% Data Used',                 16],
                      17:[None,  'K',                           17]
                      }
        
        self.station_ID()
        self.aadt()
        
    def __getitem__(self, key):
        if key in self.attrs:
            return self.attrs[key][0]
        
    def __setitem__(self, key, item):
        if key in self.attrs:
            self.attrs[key][0] = item
    
    def station_ID(self):
        self.attrs[0][0] = str(self.id)
    
    def aadt(self):
        table1 = self.aa[0]
        trs = table1.findAll('tr')
        for ind, td in enumerate(trs[-1]):
            if ind%2 == 1:
                self.attrs[ind//2][0]=str(td.string)            
