'''
Created on Feb 21, 2017

@author: Administrator
'''
import PeMS as pms
import Excel as ex

def rowtoList(records):
        rowList = []
        ind = 0
        row = []
        while ind<=24:
            row.append(records[ind])
            ind+=1
        rowList.append(row)
        return rowList
    
def idList(filename, sheetname, startRowNum=1):
    idExcel = ex.excelRead(filename, sheetname)
    idList = []
    for stationID in idExcel[startRowNum-1:]:
        stationID = str(int(stationID[0].value))
        idList.append(stationID)
    return idList

if __name__ == '__main__':
    pems = pms.PeMS()
    r, session = pems.initSession()
    print "start!"

    idList = idList("pemsIDs.xlsx", "Sheet1", startRowNum=6)
    print idList
    for stationID in idList:
        cl = pms.ChangeLog(session, stationID)
        rowList = rowtoList(cl)
        
        print rowList[0][0]        
        ex.excelWriteOnExistingFile("pems.xlsx", "Sheet1", 'A', rowList)

    