import json
import os
from rich import print
from enum import Enum

class Keys(Enum):
    LAT =  "_lat"
    LNG =  "_lng"
    ROUTEID = "_RouteId"
    ROUTEVARID = "_RouteVarId"

class Path:
    def __init__(self) -> None:
        self._RouteId = -1
        self._RouteVarId = -1
        
        self._lat = []
        self._lng = []
    
    def dic(self):
        return self.__dict__
    
    def GetRouteId(self):
        return self._RouteId
        
    def SetRouteId(self, RouteId):
        self._RouteId = RouteId
        
    def GetRouteVarId(self):
        return self._RouteVarId
        
    def SetRouteVarId(self, RouteVarId):
        self._RouteVarId = RouteVarId
        
    def Getlat(self):
        return self._lat
        
    def Setlat(self, lat):
        self._lat = lat
        
    def Getlng(self):
        return self._lng
        
    def Setlng(self, lng):
        self._lng = lng
        
class PathQuery:
    def __init__(self, fileName="paths.json"):
        self._fileName = fileName
        self._data : list[Path] = []
        
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
        data : list[Path] = []
        for line in file:
            path = Path()
            jsonList = json.loads(line)
            
            
            path.SetRouteId(jsonList['RouteId'])
            path.SetRouteVarId(jsonList['RouteVarId'])
            
            path.Setlat(jsonList['lat'])
            path.Setlng(jsonList['lng'])
            
            data.append(path)
            
        self._data = data
        return data
    
    def searchByKey(self, key = "", value = ""):
        items : list[Path] = []


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
    
    def outputAsJSON(self, items : list[Path] = []):
        if (len(items) == 0):
            items = self._data
            
        dataFolder = 'data'
        os.makedirs(dataFolder, exist_ok=True)
            
        with open(os.path.normpath(os.path.dirname(__file__) + "/" + dataFolder + "paths_filtered.json"), "w", encoding='utf8') as outfile:
            for item in items:
                diction = {}
                diction[Keys.LAT.value[1:]] = item.Getlat()
                diction[Keys.LNG.value[1:]] = item.Getlng()
                
                diction[Keys.ROUTEID.value[1:]] = item.GetRouteId()
                diction[Keys.ROUTEVARID.value[1:]] = item.GetRouteVarId()
                
                json_object = json.dumps(diction, ensure_ascii=False)
                
                outfile.write(json_object)
                outfile.write("\n")
                
        
    def outputAsCSV(self, items : list[Path] = []):
        if (len(items) == 0):
            items = self._data
            
        dataFolder = 'data'
        os.makedirs(dataFolder, exist_ok=True)
            
        with open(os.path.normpath(os.path.dirname(__file__) + "/" + dataFolder + "paths_filtered.csv"), "w", encoding='utf8') as outfile:
            outfile.write(Keys.ROUTEID.value[1:])
            outfile.write("," + Keys.ROUTEVARID.value[1:])
            outfile.write("," + Keys.LAT.value[1:])
            outfile.write("," + Keys.LNG.value[1:])
            
            outfile.write("\n")
            
            for item in items:
                outfile.write(str(item.GetRouteId()))
                outfile.write("," + str(item.GetRouteVarId()))
                
                outfile.write(",\"" + str(item.Getlat()) + "\"")
                outfile.write(",\"" + str(item.Getlng()) + "\"")
                
                outfile.write("\n")
    
if __name__ == "__main__":
    pathQr = PathQuery()
    pathQr.readFromJSON()
    data = pathQr.GetList()

    print(len(data))
    
    pathQr.outputAsCSV()