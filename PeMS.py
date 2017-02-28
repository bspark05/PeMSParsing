'''
Created on Feb 21, 2017

@author: Administrator
'''

import requests
from bs4 import BeautifulSoup

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
                      10: [None,  'Inner Median Width',             10],
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
                      24: [None,  'Lng',                            24]
                      }
        
        self.station_ID()
        self.roadway_Information()
        self.change_Log()
        
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
#         print self.attrs        
    
    def change_Log(self):
        table2 = self.cl[1]
        trs = table2.findAll('tr')
        tds = trs[-1].findAll('td')
        for ind, td in enumerate(tds):
            self.attrs[ind+16][0] = str(td.getText())
#         print self.attrs
        