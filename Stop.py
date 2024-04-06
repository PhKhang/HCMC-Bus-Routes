import json
import os
import unicodedata
from rich import print
from enum import Enum

            
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

class Stop:
    def __init__(self) -> None:
        self._StopId = -1
        self._Code = -1
        self._Name = -1
        self._StopType = -1
        self._Zone = -1
        self._Ward = -1
        self._AddressNo = -1
        self._Street = -1
        self._SupportDisability = -1
        self._Status = -1
        self._Lng = -1
        self._Lat = -1
        self._Search = -1
        self._Routes = -1
        pass
    
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

class VarStop:
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
    
    def GetAllStopId(self):
        return self._StopId 
        
    def SetAllStopId(self, StopId):
        self._StopId = StopId
    
    def GetAllCode(self):
        return self._Code 
        
    def SetAllCode(self, Code):
        self._Code = Code
    
    def GetAllName(self):
        return self._Name 
        
    def SetAllName(self, Name):
        self._Name = Name
    
    def GetAllStopType(self):
        return self._StopType 
        
    def SetStopType(self, StopType):
        self._StopType = StopType
    
    def GetAllZone(self):
        return self._Zone 
        
    def SetZone(self, Zone):
        self._Zone = Zone
    
    def GetAllWard(self):
        return self._Ward 
        
    def SetWard(self, Ward):
        self._Ward = Ward
    
    def GetAllAddressNo(self):
        return self._AddressNo 
        
    def SetAddressNo(self, AddressNo):
        self._AddressNo = AddressNo
    
    def GetAllStreet(self):
        return self._Street 
        
    def SetStreet(self, Street):
        self._Street = Street
    
    def GetAllSupportDisability(self):
        return self._SupportDisability 
        
    def SetSupportDisability(self, SupportDisability):
        self._SupportDisability = SupportDisability
    
    def GetAllStatus(self):
        return self._Status 
        
    def SetStatus(self, Status):
        self._Status = Status
    
    def GetAllLng(self):
        return self._Lng 
        
    def SetLng(self, Lng):
        self._Lng = Lng
    
    def GetAllLat(self):
        return self._Lat 
        
    def SetLat(self, Lat):
        self._Lat = Lat
    
    def GetAllSearch(self):
        return self._Search 
        
    def SetSearch(self, Search):
        self._Search = Search
    
    def GetAllRoutes(self):
        return self._Routes 
        
    def SetRoutes(self, Routes):
        self._Routes = Routes
        
        
class VarStopQuery:
    def __init__(self, fileName="stops.json"):
        self._fileName = fileName
        self._data : list[VarStop] = []
        
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
        data : list[VarStop] = []
        for line in file:
            stop = VarStop()
            jsonList = json.loads(line)
            
            stop.SetRouteId(jsonList['RouteId'])
            stop.SetRouteVarId(jsonList['RouteVarId'])
            
            stops = jsonList['Stops']
            for st in stops:
                stop.GetAllStopId().append(st['StopId'])
                stop.GetAllCode().append(st['Code'])
                stop.GetAllName().append(st['Name'])
                stop.GetAllStopType().append(st['StopType'])
                stop.GetAllZone().append(st['Zone'])
                stop.GetAllWard().append(st['Ward'])
                stop.GetAllAddressNo().append(st['AddressNo'])
                stop.GetAllStreet().append(st['Street'])
                stop.GetAllSupportDisability().append(st['SupportDisability'])
                stop.GetAllStatus().append(st['Status'])
                stop.GetAllLng().append(st['Lng'])
                stop.GetAllLat().append(st['Lat'])
                stop.GetAllSearch().append(st['Search'])
                stop.GetAllRoutes().append(st['Routes'])
                
            
            data.append(stop)
            
        self._data = data
        return data
    
    def searchByKey(self, key = "", value = ""):
        items : list[VarStop] = []
        
        value = unicodedata.normalize("NFC", value)

        if (key == ""):
            return items;
        
        for routeVar in self._data:
            if isinstance(routeVar.dict()[key], list):
                # print("A list")
                for i in routeVar.dict()[key]:
                    if unicodedata.normalize("NFC", str(i)) == value:
                        print(str(i) + "," + value)
                        print(unicodedata.normalize("NFC", str(i)) == value)
                        items.append(routeVar)
                        break;
            else:
                # print("Not a list")
                # print(str(routeVar.dict()[key]) + "," + value)
                if unicodedata.normalize("NFC", str(routeVar.dict()[key])) == value:
                    items.append(routeVar)
                
            pass
        
        # self._data = items
        newInstance = VarStopQuery()
        newInstance.SetList(items)
        return newInstance
    
    def outputAsJSON(self, items : list[VarStop] = []):
        if (len(items) == 0):
            items = self._data
            
        dataFolder = 'data'
        os.makedirs(dataFolder, exist_ok=True)
        
        with open(os.path.normpath(os.path.dirname(__file__) + "/" + dataFolder + "/stops_filtered.json"), "w", encoding='utf8') as outfile:
            for item in items:
                for i in range(0, len(item.GetAllStopId())):
                    diction = {}
                    diction[Keys.ROUTEID.value[1:]] = item.GetRouteId()
                    diction[Keys.ROUTEVARID.value[1:]] = item.GetRouteVarId()
                    
                    diction[Keys.STOPID.value[1:]] = item.GetAllStopId()[i]
                    diction[Keys.CODE.value[1:]] = item.GetAllCode()[i]
                    diction[Keys.NAME.value[1:]] = item.GetAllName()[i]
                    diction[Keys.STOPID.value[1:]] = item.GetAllStopType()[i]
                    diction[Keys.ZONE.value[1:]] = item.GetAllZone()[i]
                    diction[Keys.WARD.value[1:]] = item.GetAllWard()[i]
                    diction[Keys.ADDRESSNO.value[1:]] = item.GetAllAddressNo()[i]
                    diction[Keys.STREET.value[1:]] = item.GetAllStreet()[i]
                    diction[Keys.SUPPORTDISABILITY.value[1:]] = item.GetAllSupportDisability()[i]
                    diction[Keys.STATUS.value[1:]] = item.GetAllStatus()[i]
                    diction[Keys.LNG.value[1:]] = item.GetAllLng()[i]
                    diction[Keys.LAT.value[1:]] = item.GetAllLat()[i]
                    diction[Keys.SEARCH.value[1:]] = item.GetAllSearch()[i]
                    diction[Keys.ROUTES.value[1:]] = item.GetAllRoutes()[i]
                    
                    json_object = json.dumps(diction, ensure_ascii=False)
                    
                    outfile.write(json_object)
                    outfile.write("\n")
            
    def outputAsCSV(self, items : list[VarStop] = []):
        if (len(items) == 0):
            items = self._data
            
        dataFolder = 'data'
        os.makedirs(dataFolder, exist_ok=True)
        
        with open(os.path.normpath(os.path.dirname(__file__) + "/" + dataFolder + "/stops_filtered.csv"), "w", encoding='utf8') as outfile:
            firstColumn = True
            for key in Keys:
                if not firstColumn:
                    outfile.write(",")
                    
                outfile.write(key.value[1:])
                firstColumn = False
            
            outfile.write("\n")
            
            for item in items:
                for i in range(0, len(item.GetAllStopId())):
                    outfile.write(str(item.GetRouteId()))
                    outfile.write("," + str(item.GetRouteVarId()))
                
                    outfile.write("," + str(item.GetAllStopId()[i]))
                    outfile.write("," + str(item.GetAllCode()[i]))
                    outfile.write("," + str(item.GetAllName()[i]))
                    outfile.write("," + str(item.GetAllStopType()[i]))
                    outfile.write("," + str(item.GetAllZone()[i]))
                    outfile.write("," + str(item.GetAllWard()[i]))
                    outfile.write("," + str(item.GetAllAddressNo()[i]))
                    outfile.write("," + str(item.GetAllStreet()[i]))
                    outfile.write("," + str(item.GetAllSupportDisability()[i]))
                    outfile.write("," + str(item.GetAllStatus()[i]))
                    outfile.write("," + str(item.GetAllLng()[i]))
                    outfile.write("," + str(item.GetAllLat()[i]))
                    outfile.write("," + str(item.GetAllSearch()[i]))
                    outfile.write(",\"" + str(item.GetAllRoutes()[i]) + "\"")
                    
                    outfile.write("\n")
            
if __name__ == "__main__":
    query = VarStopQuery()
    
    query.readFromJSON()
    # stopQr.
    print(len(query.GetList()))

    datadata = query.searchByKey("_StopId", '35').GetList()
    
    print(len(datadata))
    
    print(datadata[0].dict())
    
    # stopQr.outputAsCSV()
    # stopQr.outputAsJSON()