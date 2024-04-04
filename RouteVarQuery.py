import json
import os
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
        self._RouteVarId = []
        self._RouteVarName = []
        self._RouteVarShortName = []
        self._RouteNo = []
        self._StartStop = []
        self._EndStop = []
        self._Distance = []
        self._Outbound = []
        self._RunningTime = []
        
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
            routeVar = RouteVar()
            jsonList = json.loads(line)
            
            if (len(jsonList) == 0): # Remove empty JSON list
                continue
            
            routeVar.SetRouteId(jsonList[0]['RouteId'])
            for var in jsonList:
                routeVar.GetRouteVarId().append(var['RouteVarId'])
                routeVar.GetRouteVarName().append(var['RouteVarName'])
                routeVar.GetRouteVarShortName().append(var['RouteVarShortName'])
                routeVar.GetRouteNo().append(var['RouteNo'])
                routeVar.GetStartStop().append(var['StartStop'])
                routeVar.GetEndStop().append(var['EndStop'])
                routeVar.GetDistance().append(var['Distance'])
                routeVar.GetOutbound().append(var['Outbound'])
                routeVar.GetRunningTime().append(var['RunningTime'])
            
            data.append(routeVar)
        self._data = data
        return data
    
    def searchByKey(self, key = "", value = ""):
        items : list[RouteVar] = []

        if (key == ""):
            return items;
        
        for routeVar in self._data:
            if isinstance(routeVar.dict()[key], list):
                # print("A list")
                for i in routeVar.dict()[key]:
                    if i == value:
                        items.append(routeVar)
                        break;
            else:
                # print("Not a list")
                if routeVar.dict()[key] == value:
                    items.append(routeVar)
                
            pass
        
        self._data = items
        return self
    
    def outputAsJSON(self, items : list[RouteVar] = []):
        if (len(items) == 0):
            items = self._data
            
        dataFolder = 'data'
        os.makedirs(dataFolder, exist_ok=True)
        
        with open(os.path.normpath(os.path.dirname(__file__) + "/" + dataFolder + "/sample.json"), "w", encoding='utf8') as outfile:
            for item in items:
                for i in range(0, len(item.GetRouteVarId())):
                    diction = {}
                    diction[Keys.ROUTEID.value[1:]] = item.GetRouteId()
                    
                    diction[Keys.ROUTEVARID.value[1:]] = item.GetRouteVarId()[i]
                    diction[Keys.ROUTEVARNAME.value[1:]] = item.GetRouteVarName()[i]
                    diction[Keys.ROUTEVARSHORTNAME.value[1:]] = item.GetRouteVarShortName()[i]
                    diction[Keys.ROUTENO.value[1:]] = item.GetRouteNo()[i]
                    diction[Keys.STARTSTOP.value[1:]] = item.GetStartStop()[i]
                    diction[Keys.ENDSTOP.value[1:]] = item.GetEndStop()[i]
                    diction[Keys.DISTANCE.value[1:]] = item.GetDistance()[i]
                    diction[Keys.OUTBOUND.value[1:]] = item.GetOutbound()[i]
                    diction[Keys.RUNNINGTIME.value[1:]] = item.GetRunningTime()[i]
                    
                    json_object = json.dumps(diction, ensure_ascii=False)
                    
                    outfile.write(json_object)
                    outfile.write("\n")
                    
    def outputAsCSV(self, items : list[RouteVar] = []):
        if (len(items) == 0):
            items = self._data
            
        dataFolder = 'data'
        os.makedirs(dataFolder, exist_ok=True)
        
        with open(os.path.normpath(os.path.dirname(__file__) + "/" + dataFolder + "/sample.csv"), "w", encoding='utf8') as outfile:
            firstColumn = True
            for key in Keys:
                if not firstColumn:
                    outfile.write(",")
                    
                outfile.write(key.value[1:])
                firstColumn = False
            
            outfile.write("\n")
                
            for item in items:
                for i in range(0, len(item.GetRouteVarId())):
                    outfile.write(str(item.GetRouteId()))
                    
                    outfile.write("," + str(item.GetRouteVarId()[i]))
                    outfile.write("," + str(item.GetRouteVarName()[i]))
                    outfile.write("," + str(item.GetRouteVarShortName()[i]))
                    outfile.write("," + str(item.GetRouteNo()[i]))
                    outfile.write("," + str(item.GetStartStop()[i]))
                    outfile.write("," + str(item.GetEndStop()[i]))
                    outfile.write("," + str(item.GetDistance()[i]))
                    outfile.write("," + str(item.GetOutbound()[i]))
                    outfile.write("," + str(item.GetRunningTime()[i]))
                    
                    outfile.write("\n")
                    
            
    
if __name__ == "__main__":
    routeVarQuery = RouteVarQuery()
    routeVarQuery.readFromJSON()

    data = routeVarQuery.searchByKey(Keys.STARTSTOP.value, "Bến xe buýt Sài Gòn").GetList()

    print(len(data))
    
    routeVarQuery.outputAsCSV()
    routeVarQuery.outputAsJSON()
    
    # with open("thing.csv", "w", encoding='utf8') as outfile:
    #     for key in Keys:
    #         outfile.write(key.value)
    #         outfile.write(",")
    
    # for d in data:
    #     print(d.dict())
