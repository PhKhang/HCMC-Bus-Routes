import json
import os
import unicodedata
from rich import print
from enum import Enum


class Keys(Enum):
    ROUTEID = "_RouteId"
    ROUTEVARID = "_RouteVarId"
    ROUTEVARNAME = "_RouteVarName"
    ROUTEVARSHORTNAME = "_RouteVarShortName"
    ROUTENO = "_RouteNo"
    STARTSTOP = "_StartStop"
    ENDSTOP = "_EndStop"
    DISTANCE = "_Distance"
    OUTBOUND = "_Outbound"
    RUNNINGTIME = "_RunningTime"

class RouteVar:
    def __init__(self):
        self._RouteId = -1
        self._RouteVarId = -1
        self._RouteVarName = -1
        self._RouteVarShortName = -1
        self._RouteNo = -1
        self._StartStop = -1
        self._EndStop = -1
        self._Distance = -1
        self._Outbound = -1
        self._RunningTime = -1
        
    def __str__(self):
        return self.__dict__
    
    def dict(self):
        return self.__dict__
    
    def GetRouteId(self):
        return self._RouteId

    def SetRouteId(self, RouteId):
        self._RouteId = RouteId

    def GetRouteVarId(self):
        return self._RouteVarId

    def SetRouteVarId(self, RouteVarId):
        self._RouteVarId = RouteVarId

    def GetRouteVarName(self):
        return self._RouteVarName

    def SetRouteVarName(self, RouteVarName):
        self._RouteVarName = RouteVarName

    def GetRouteVarShortName(self):
        return self._RouteVarShortName

    def SetRouteVarShortName(self, RouteVarShortName):
        self._RouteVarShortName = RouteVarShortName

    def GetRouteNo(self):
        return self._RouteNo

    def SetRouteNo(self, RouteNo):
        self._RouteNo = RouteNo

    def GetStartStop(self):
        return self._StartStop

    def SetStartStop(self, StartStop):
        self._StartStop = StartStop

    def GetEndStop(self):
        return self._EndStop

    def SetEndStop(self, EndStop):
        self._EndStop = EndStop

    def GetDistance(self):
        return self._Distance

    def SetDistance(self, Distance):
        self._Distance = Distance

    def GetOutbound(self):
        return self._Outbound

    def SetOutbound(self, Outbound):
        self._Outbound = Outbound

    def GetRunningTime(self):
        return self._RunningTime

    def SetRunningTime(self, RunningTime):
        self._RunningTime = RunningTime


class RouteVarQuery:
    def __init__(self, fileName="vars.json"):
        self._fileName = fileName
        self._data : list[RouteVar] = []

    def GetList(self):
        return self._data
    
    def SetList(self, data):
        self._data = data
    
    def GetFileName(self):
        return self._fileName
    
    def SetFileName(self, fileName):
        self._fileName = fileName

    def readFromJSON(self):
        file = open(os.path.normpath(os.path.dirname(__file__) + "/data/" + self._fileName), encoding='utf-8')
        data = []
        for line in file:
            jsonList = json.loads(line)
            
            if (len(jsonList) == 0): # Remove empty JSON list
                continue
            
            for var in jsonList:
                routeVar = RouteVar()
                routeVar.SetRouteId(var['RouteId'])
                routeVar.SetRouteVarId((var['RouteVarId']))
                routeVar.SetRouteVarName((var['RouteVarName']))
                routeVar.SetRouteVarShortName((var['RouteVarShortName']))
                routeVar.SetRouteNo((var['RouteNo']))
                routeVar.SetStartStop((var['StartStop']))
                routeVar.SetEndStop((var['EndStop']))
                routeVar.SetDistance((var['Distance']))
                routeVar.SetOutbound((var['Outbound']))
                routeVar.SetRunningTime((var['RunningTime']))
            
                data.append(routeVar)
                
        self._data = data
        return data
    
    def searchByKey(self, key = "", value = "", modify = False):
        items : list[RouteVar] = []

        value = unicodedata.normalize("NFC", value)

        if (key == ""):
            return items
        
        for routeVar in self._data:
            if isinstance(routeVar.dict()[key], list):
                # print("A list")
                for i in routeVar.dict()[key]:
                    if unicodedata.normalize("NFC", str(i)) == value:
                        items.append(routeVar)
                        break
            else:
                # print("Not a list")
                if unicodedata.normalize("NFC", str(routeVar.dict()[key])).lower() == value.lower():
                    items.append(routeVar)
                
            pass
        
        if modify == False:
            newInstance = RouteVarQuery()
            newInstance.SetList(items)
            return newInstance
        
        self._data = items
        return self
    
    def outputAsJSON(self, items : list[RouteVar] = []):
        if (len(items) == 0):
            items = self._data
            
        dataFolder = 'data'
        os.makedirs(dataFolder, exist_ok=True)
        
        with open(os.path.normpath(os.path.dirname(__file__) + "/" + dataFolder + "/vars_filtered.json"), "w", encoding='utf8') as outfile:
            for item in items:
                diction = {}
                diction[Keys.ROUTEID.value[1:]] = item.GetRouteId()
                
                diction[Keys.ROUTEVARID.value[1:]] = item.GetRouteVarId()
                diction[Keys.ROUTEVARNAME.value[1:]] = item.GetRouteVarName()
                diction[Keys.ROUTEVARSHORTNAME.value[1:]] = item.GetRouteVarShortName()
                diction[Keys.ROUTENO.value[1:]] = item.GetRouteNo()
                diction[Keys.STARTSTOP.value[1:]] = item.GetStartStop()
                diction[Keys.ENDSTOP.value[1:]] = item.GetEndStop()
                diction[Keys.DISTANCE.value[1:]] = item.GetDistance()
                diction[Keys.OUTBOUND.value[1:]] = item.GetOutbound()
                diction[Keys.RUNNINGTIME.value[1:]] = item.GetRunningTime()
                
                json_object = json.dumps(diction, ensure_ascii=False)
                
                outfile.write(json_object)
                outfile.write("\n")
                    
    def outputAsCSV(self, items : list[RouteVar] = []):
        if (len(items) == 0):
            items = self._data
            
        dataFolder = 'data'
        os.makedirs(dataFolder, exist_ok=True)
        
        with open(os.path.normpath(os.path.dirname(__file__) + "/" + dataFolder + "/vars_filtered.csv"), "w", encoding='utf8') as outfile:
            firstColumn = True
            for key in Keys:
                if not firstColumn:
                    outfile.write(",")
                    
                outfile.write(key.value[1:])
                firstColumn = False
            
            outfile.write("\n")
                
            for item in items:
                outfile.write(str(item.GetRouteId()))
                
                outfile.write("," + str(item.GetRouteVarId()))
                outfile.write("," + str(item.GetRouteVarName()))
                outfile.write("," + str(item.GetRouteVarShortName()))
                outfile.write("," + str(item.GetRouteNo()))
                outfile.write("," + str(item.GetStartStop()))
                outfile.write("," + str(item.GetEndStop()))
                outfile.write("," + str(item.GetDistance()))
                outfile.write("," + str(item.GetOutbound()))
                outfile.write("," + str(item.GetRunningTime()))
                
                outfile.write("\n")
                    
            
    
if __name__ == "__main__":
    routeVarQuery = RouteVarQuery()
    routeVarQuery.readFromJSON()

    # data = routeVarQuery.searchByKey(Keys.ROUTEVARID.value, "1").GetList()
    # print(len(data))

    
    data = routeVarQuery.searchByKey(Keys.ENDSTOP.value, "thạnh lộc").GetList()
    print(len(data))
    
    for da in data:
        print(da.dict())

    
    routeVarQuery.outputAsCSV()
    routeVarQuery.outputAsJSON()
    
    # with open("thing.csv", "w", encoding='utf8') as outfile:
    #     for key in Keys:
    #         outfile.write(key.value)
    #         outfile.write(",")
    
    # for d in data:
    #     print(d.dict())
