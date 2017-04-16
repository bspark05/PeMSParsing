'''
Created on Apr 14, 2017

@author: Administrator
'''
from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datetime
import time
from time import sleep

class PeMS2:
    def __init__(self):
        self.url = 'http://pems.dot.ca.gov/'
        
    def initSession(self):
        username = 'bumsubp@uci.edu'
        password = 'javawm'
         
        xpaths = { 'username' : "//input[@name='username']",
                  'password': "//input[@name='password']",
                  'submit':"//input[@name='login']"
                 }
        
        driver = webdriver.Firefox()
        driver.get(self.url)
        driver.maximize_window()
        
        #Clear Username TextBox if already allowed "Remember Me" 
        driver.find_element_by_xpath(xpaths['username']).clear()
        
        #Write Username in Username TextBox
        driver.find_element_by_xpath(xpaths['username']).send_keys(username)
        
        #Clear Password TextBox if already allowed "Remember Me" 
        driver.find_element_by_xpath(xpaths['password']).clear()
        
        #Write Password in password TextBox
        driver.find_element_by_xpath(xpaths['password']).send_keys(password)
        
        #Click Login button
        driver.find_element_by_xpath(xpaths['submit']).click()
        
        return driver
        
class DayOfWeek:
    def __init__(self, driver, id):
        self.id = str(id)
        sDate = datetime.date(2016, 1, 1)
        eDate = datetime.date(2016, 12, 31)
        sUnixtime = str(int(time.mktime(sDate.timetuple())))
        eUnixtime = str(int(time.mktime(eDate.timetuple())))
        
        urlDoW = "http://pems.dot.ca.gov/?s_time_id="+sUnixtime+"&e_time_id="+eUnixtime+"&html_x=33&report_form=1&tod=all&tod_from=0&tod_to=0&dnode=VDS&content=loops&tab=det_dow&station_id="+id
        driver.get(urlDoW)
        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@title="Link to incident report"]')))
        sleep(0.5)
            
        soup = BeautifulSoup(driver.page_source,"lxml")
        self.incident = soup.findAll('div', attrs={"class": "count", "id":"incidentCount"})
        
        self.attrs = {
                      0: [None,  'StationID',                   0],
                      1: [None,  'Incident',                    1],
                      2: [None,  'IncidentURL',                 2]
                      }
        
        self.station_ID()
        self.accident()
        
    def __getitem__(self, key):
        if key in self.attrs:
            return self.attrs[key][0]
        
    def __setitem__(self, key, item):
        if key in self.attrs:
            self.attrs[key][0] = item
            
    def station_ID(self):
        self.attrs[0][0] = str(self.id)
            
    def accident(self):
        incidentVal = self.incident[0].find('a').get_text()
        incidentA = self.incident[0].find('a', href=True)['href']
         
        self.attrs[1][0]=str(incidentVal)
        self.attrs[2][0]=str(incidentA)
        
#         print incidentA
#         print incidentVal
        