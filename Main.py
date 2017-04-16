'''
Created on Feb 21, 2017

@author: Administrator
'''
# import PeMS as pms
import Excel as ex
import PeMS2 as pms2

def rowtoList(records):
        rowList = []
        ind = 0
        row = []
        while ind<=44:
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
    pems2=pms2.PeMS2()
    driver = pems2.initSession()
    print "start!"
    
    idList = idList("peMS_ID_HOV.xlsx", "LA", startRowNum=2)
    print idList
    for stationID in idList:
        acci = pms2.DayOfWeek(driver, stationID)
        rowList = rowtoList(acci)
        
        print rowList[0][0]
        ex.excelWriteOnExistingFile("peMS_Accident_HOV.xlsx", "LA", 'A', rowList)
      
            
#     pems = pms.PeMS()
#     r, session = pems.initSession()
#     print "start!"
    
#     idList = idList("peMS_ID_Mainline.xlsx", "LA", startRowNum=2)
#     print idList
#     for stationID in idList:
#         cl = pms.ChangeLog(session, stationID)
#         rowList = rowtoList(cl)
#           
#         print rowList[0][0]        
#         ex.excelWriteOnExistingFile("peMS_Station_Mainline.xlsx", "LA", 'A', rowList)

    
#     idList = idList("peMS_ID_Mainline.xlsx", "LA", startRowNum=2)
#     print idList
#     for stationID in idList:
#         aadt = pms.Performance(session, stationID)
#         rowList = rowtoList(aadt)
#           
#         print rowList[0][4]        
#         ex.excelWriteOnExistingFile("peMS_AADT_Mainline.xlsx", "LA", 'A', rowList)
        