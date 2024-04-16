import json
import os
import Path
import Stop
from rich import print

empty = {
  "type": "FeatureCollection",
  "features": []
}

def addPoint(dic, lng, lat, name = "", color = "", size = "", symbol = ""):
    template = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [lng, lat],
        "type": "Point"
      }
    }
    
    if (name != ""):
        template['properties']['name'] = name
      
    if (color != ""):
        template['properties']['marker-color'] = color
        
    if (size != ""):
        template['properties']['marker-size'] = size
        
    if (symbol != ""):
        template['properties']['marker-symbol'] = symbol
        
    dic['features'].append(template)

def addLine(dic, lng, lat, name = "", color = "", strokeWidth = "", strokeOpacity = ""):
    template = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [],
        "type": "LineString"
      }
    }
    
    if (name != ""):
        template['properties']['name'] = name
      
    if (color != ""):
        template['properties']['stroke'] = color
        
    if (size != ""):
        template['properties']['strok-width'] = strokeWidth
        
    if (symbol != ""):
        template['properties']['stroke-opacity'] = strokeOpacity
        
    for i in range(len(lat)):
        template['geometry']['coordinates'].append([lng[i], lat[i]])
        
    dic['features'].append(template)



def writeGeoJson(content):
    with open(os.path.normpath(os.path.dirname(__file__) + "/geoJson.json"), 'w') as file:
        file.write(json.dumps(content, indent=4))
        
    print("Wrote to file successfully")

def loadGeoJson():
    file = open(os.path.normpath(os.path.dirname(__file__) + "/geoJson.json"))
    data = json.load(file)
    print("URL link:")
    url = "http://geojson.io/#data=data:application/json," + str(data)
    url = url.replace("\'", "\"")
    print(url)
    try:
        os.startfile(url)
    except:
        print("URL too long to open a browser")
    

if __name__ == "__main__":
    query = Path.PathQuery()
    query.readFromJSON()
    
    paths = query.searchByKey(Path.Keys.ROUTEVARID.value, "5").GetList()
    
    print(len(query.GetList()))
    
    qr = Stop.VarStopQuery()
    qr.readFromJSON()
    stops = qr.searchByKey(Stop.Keys.ROUTEVARID.value, "5").GetList()
    
    # print(len(qr.GetList()))
    index = 0
    for pathPoint in paths:
      for i in range(len(pathPoint.Getlat())):
        addPoint(empty, pathPoint.Getlng()[i], pathPoint.Getlat()[i], "Path " + str(index), "#696969")
        index += 1
        
    index = 0
    for stop in stops:
        for i in range(len(stop.GetAllLat())):
            addPoint(empty, stop.GetAllLng()[i], stop.GetAllLat()[i], "Stop " + str(stop.GetAllStopId()[i]), "#e01")
            index += 1
    
    
    writeGeoJson(empty)
    loadGeoJson()
# http://geojson.io/#data=data:application/json,{"type": "Feature", "geometry": {"type": "Point", "coordinates": [125.6, 10.1]}, "properties": {"name": "Dinagat Islands"}}