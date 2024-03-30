import json
from rich import print
from enum import Enum

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
    def __init__(self, fileName="vars.json"):
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
        file = open(file='paths.json', encoding='utf-8')
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
    
pathQr = PathQuery()
pathQr.readFromJSON()
data = pathQr.GetList()

print(data[0].Getlat())