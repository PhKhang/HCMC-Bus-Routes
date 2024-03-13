import json

class RouteVar:
  def __init__(self, dict = None):
    self._RouteId = dict.get('RouteId')
    self._RouteVarId = dict.get('RouteVarId')
    self._RouteVarName = dict.get('RouteVarName')
    self._RouteVarShortName = dict.get('RouteVarShortName')
    self._RouteNo = dict.get('RouteNo')
    self._StartStop = dict.get('StartStop')
    self._EndStop = dict.get('EndStop')
    self._Distance = dict.get('Distance')
    self._Outbound = dict.get('Outbound')
    self._RunningTime = dict.get('RunningTime')
    
  @property
  def RouteId(self):
    return self._RouteId
  
  @RouteId.setter
  def RouteId(self, RouteId):
    self._RouteId = RouteId
    
  @property
  def RouteVarId(self):
    return self._RouteVarId
    
  @RouteVarId.setter
  def RouteVarId(self, RouteVarId):
    self._RouteVarId = RouteVarId
    
  @property
  def RouteVarName(self):
    return self._RouteVarName
    
  @RouteVarName.setter
  def RouteVarName(self, RouteVarName):
    self._RouteVarName = RouteVarName
    
  @property
  def RouteVarShortName(self):
    return self._RouteVarShortName
    
  @RouteVarShortName.setter
  def RouteVarShortName(self, RouteVarShortName):
    self._RouteVarShortName = RouteVarShortName
    
  @property
  def RouteNo(self):
    return self._RouteNo
    
  @RouteNo.setter
  def RouteNo(self, RouteNo):
    self._RouteNo = RouteNo
    
  @property
  def StartStop(self):
    return self._StartStop
    
  @StartStop.setter
  def StartStop(self, StartStop):
    self._StartStop = StartStop
    
  @property
  def EndStop(self):
    return self._EndStop
    
  @EndStop.setter
  def EndStop(self, EndStop):
    self._EndStop = EndStop
    
  @property
  def Distance(self):
    return self._Distance
    
  @Distance.setter
  def Distance(self, Distance):
    self._Distance = Distance
    
  @property
  def Outbound(self):
    return self._Outbound
    
  @Outbound.setter
  def Outbound(self, Outbound):
    self._Outbound = Outbound
    
  @property
  def RunningTime(self):
    return self._RunningTime    
    
  @RunningTime.setter
  def RunningTime(self, RunningTime):
    self._RunningTime = RunningTime
    
    
class RouteVarQuery:
  def __init__(self, fileName = None):
    if not fileName:
      
      pass
        

c = RouteVar
# c.RouteId = 89

# print(c.RouteId)

file = open(file='vars.json', encoding='utf-8')
data = list
for line in file:
  jsonList = json.loads(line)
  print(jsonList)
  data.append(jsonList)
  break
  
print(len(data))
print(data[0].get('RouteId'))