import json
from rich import print
from enum import Enum


class Stop:
    def __init__(self) -> None:
        self._RouteId = -1
        self._RouteVarId = -1
        
        self._StopId = []
        self._Code = []
        self._Name = []
        self._StopType = []
        self._Zone = []
        self._Ward = []
        self._AddressNo = []
        self._Street = []
        self._SupportDisability = []
        self._Status = []
        self._Lng = []
        self._Lat = []
        self._Search = []
        self._Routes = []
    
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
    
    def GetStopId(self):
        return self._StopId 
        
    def SetStopId(self, StopId):
        self._StopId = StopId
    
    def GetCode(self):
        return self._Code 
        
    def SetCode(self, Code):
        self._Code = Code
    
    def GetName(self):
        return self._Name 
        
    def SetName(self, Name):
        self._Name = Name
    
    def GetStopType(self):
        return self._StopType 
        
    def SetStopType(self, StopType):
        self._StopType = StopType
    
    def GetZone(self):
        return self._Zone 
        
    def SetZone(self, Zone):
        self._Zone = Zone
    
    def GetWard(self):
        return self._Ward 
        
    def SetWard(self, Ward):
        self._Ward = Ward
    
    def GetAddressNo(self):
        return self._AddressNo 
        
    def SetAddressNo(self, AddressNo):
        self._AddressNo = AddressNo
    
    def GetStreet(self):
        return self._Street 
        
    def SetStreet(self, Street):
        self._Street = Street
    
    def GetSupportDisability(self):
        return self._SupportDisability 
        
    def SetSupportDisability(self, SupportDisability):
        self._SupportDisability = SupportDisability
    
    def GetStatus(self):
        return self._Status 
        
    def SetStatus(self, Status):
        self._Status = Status
    
    def GetLng(self):
        return self._Lng 
        
    def SetLng(self, Lng):
        self._Lng = Lng
    
    def GetLat(self):
        return self._Lat 
        
    def SetLat(self, Lat):
        self._Lat = Lat
    
    def GetSearch(self):
        return self._Search 
        
    def SetSearch(self, Search):
        self._Search = Search
    
    def GetRoutes(self):
        return self._Routes 
        
    def SetRoutes(self, Routes):
        self._Routes = Routes
        
        
class StopQuery:
    def __init__(self, fileName="vars.json"):
        self._fileName = fileName
        self._data : list[Stop] = []
        
    def GetList(self):
        return self._data
    
    def SetList(self, data):
        self._data = data
    
    def GetFileName(self):
        return self._fileName
    
    def SetFileName(self, fileName):
        self._fileName = fileName
        
    def readFromJSON(self):
        file = open(file='stops.json', encoding='utf-8')
        data : list[Stop] = []
        for line in file:
            stop = Stop()
            jsonList = json.loads(line)
            
            stops = jsonList['Stops']
            
            stop.SetRouteId(jsonList['RouteId'])
            stop.SetRouteVarId(jsonList['RouteVarId'])
            for st in stops:
                stop.GetStopId().append(st['StopId'])
                stop.GetCode().append(st['Code'])
                stop.GetName().append(st['Name'])
                stop.GetStopType().append(st['StopType'])
                stop.GetZone().append(st['Zone'])
                stop.GetWard().append(st['Ward'])
                stop.GetAddressNo().append(st['AddressNo'])
                stop.GetStreet().append(st['Street'])
                stop.GetSupportDisability().append(st['SupportDisability'])
                stop.GetStatus().append(st['Status'])
                stop.GetLng().append(st['Lng'])
                stop.GetLat().append(st['Lat'])
                stop.GetSearch().append(st['Search'])
                stop.GetRoutes().append(st['Routes'])
                
            
            data.append(stop)
            
        self._data = data
        return data
    
    def searchByKey(self, key = "", value = ""):
        items : list[Stop] = []


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
            
            
class Keys(Enum):
    ROUTEID =  "_RouteId"
    ROUTEVARID =  "_RouteVarId"
    STOPID = "_StopId"
    CODE = "_Code"
    NAME = "_Name"
    STOPTYPE = "_StopType"
    ZONE = "_Zone"
    WARD = "_Ward"
    ADDRESSNO = "_AddressNo"
    STREET = "_Street"
    SUPPORTDISABILITY = "_SupportDisability"
    STATUS = "_Status"
    LNG = "_Lng"
    LAT = "_Lat"
    SEARCH = "_Search"
    ROUTES = "_Routes"
            
stopQr = StopQuery()
(len(stopQr.readFromJSON()))

query = stopQr.searchByKey(Keys.ROUTEID.value, '3').GetList()

# print(query[0])
print(len(query))