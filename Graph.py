from math import sqrt
from networkx import connected_components
from pyproj import Proj, Geod
from shapely import LineString, Point, MultiPoint
from rtree import index
from rich import print
import matplotlib.pyplot as plt
import networkx
import Path
import Stop
import RouteVar

def findNextClosest(pathIndex, currentStop, coordPoints):
    closestIndex = pathIndex + 1
    if closestIndex >= len(coordPoints):
        print("Out of point on path")
        return pathIndex
    
    
    idx = index.Index()
    
    listOfPathPoint = coordPoints[pathIndex + 1 : min(pathIndex + 50, len(coordPoints) - 1)]
    
    # print("-------------")
    closestPointId = -1
    for p in range(len(listOfPathPoint)):
        # print(p, ". ", end="")
        idx.insert(pathIndex + 1 + p, (listOfPathPoint[p][0], listOfPathPoint[p][1], listOfPathPoint[p][0], listOfPathPoint[p][1]))
        # print(pathIndex + 1 + p, (listOfPathPoint[p][0], listOfPathPoint[p][1], listOfPathPoint[p][0], listOfPathPoint[p][1]))
        # print("->", currentStop[0], currentStop[1], currentStop[0], currentStop[1])
        closestPointId = list(idx.nearest((currentStop[0], currentStop[1], currentStop[0], currentStop[1]), 1))[0]
    
    # print("Len: ", len(list(idx.nearest((currentStop[0], currentStop[1], currentStop[0], currentStop[1]), 1))))
    return closestPointId
            

# 1.Xây dựng graph trong đó: đỉnh là stop, cạnh là các cung liền kề của tuyến xe bus,
# trọng số là thời gian (second). SV dựa vào giờ bắt đầu của tuyến xe, (lat, lng) để tính được thời gian “tương đối” giữa 2 đỉnh liền kề. SV nhớ đổi (lat, lng) sang (x, y) trước khi thực hiện. Với mỗi cạnh lưu cả trọng số thời gian (second) và trọng số khoảng cách (m).

# 2. Tự cài đặt giải thuật Dijkstra, tìm đường đi ngắn nhất giữa
# tất cả các cặp đỉnh trong graph (all pairs). Lưu kết quả vào file.

# 3. Chọn (start_stop, end_stop), export dạng json đường đi ngắn nhất giữa 2 stop. 
# Export kèm theo các path của các route tương ứng để đối chiếu đường đi có phù hợp hay ko?

# 4. Tính và hiển thị top k = 10 (default) stop có độ quan trọng cao nhất. 
# Export dạng json có kèm theo id, số liệu, lat, lng, tên stop. 
# Cách tính: cứ có 1 shortest path đi qua stop A thì count(stopA) tăng 1.

def createPath(graph: networkx.MultiDiGraph, stopIdNode: list[str], stopPoints: list[tuple], pathPoints: list[tuple], runningTime, routeVarId):
    pathIndex = -1
    totalLength = LineString(pathPoints).length
    for i in range(len(stopIdNode)):
        if pathIndex == -1:
            pathIndex += 1
            continue
        
        closestIndex = findNextClosest(pathIndex, stopPoints[i], pathPoints)
        line = LineString(pathPoints[pathIndex : closestIndex + 1])
        pathIndex = closestIndex
        # print(stopIdNode[i - 1], stopIdNode[i], line.length)
        graph.add_edge(stopIdNode[i - 1], stopIdNode[i], time = runningTime / totalLength * line.length, dis = line.length, routeVar = routeVarId)
        networkx.set_node_attributes(graph, {stopIdNode[i - 1]: {"coord": stopPoints[i - 1]}})
        # print({stopIdNode[i - 1]: {"coord": stopPoints[i - 1]}})
        networkx.set_node_attributes(graph, {stopIdNode[i]: {"coord": stopPoints[i]}})
        # print({stopIdNode[i]: {"coord": stopPoints[i]}})
        
    return graph


def connectGraph(subGraphs: list[networkx.MultiDiGraph]):
    connectionPair = []
    for i in range(len(subGraphs)):
        for j in range(i + 1, len(subGraphs)):
            idx = index.Index()
            
            nodeCoordI = networkx.get_node_attributes(subGraphs[i], 'coord')
            
            iNodes = list(subGraphs[i].nodes)
            jNodes = list(subGraphs[j].nodes)
            # print(len(list(subGraphs[i].nodes)))
            # print(subGraphs[i].nodes[7278]['coord'])
            # print(subGraphs[i].has_node(7276))
            
            for node in iNodes:
                idx.insert(node, (nodeCoordI[node][0], nodeCoordI[node][1], nodeCoordI[node][0], nodeCoordI[node][1]))
                
            # print(jNodes)
            minDisSoFar = -1
            connection1 = -1
            connection2 = -1
            for node in jNodes:
                # print(subGraphs[j].nodes[7529]['coord'])
                x, y = subGraphs[j].nodes[node]['coord']
                nearestId = list(idx.nearest((x, y, x, y), 1))[0]
                x1, y1 = nodeCoordI[nearestId]
                
                dis = sqrt((x - x1)**2 + (y - y1)**2)
                if minDisSoFar == -1 or minDisSoFar > dis:
                    minDisSoFar = dis
                    connection1 = node
                    connection2 = nearestId
                    
            
            if connection1 == 1:
                print("No points found")
                return
            
            # Only connect two stops that are less than 1km apart
            if minDisSoFar < 1000:
                connectionPair.append((connection1, connection2, minDisSoFar))
                
    return connectionPair

def buildGraph():
    
    allVar = RouteVar.RouteVarQuery()
    allVar.readFromJSON()
    
    findPath = Path.PathQuery()
    findPath.readFromJSON()
    
    findStop = Stop.VarStopQuery()
    findStop.readFromJSON()
    
    itCount = 1
    limit = 1
    graph = networkx.MultiDiGraph()
    for var in allVar.GetList():
        # if itCount > limit:
        #     break
        # itCount += 1
        
        routId = str(var.GetRouteId())
        routVarId = str(var.GetRouteVarId())
        
        print(f"Making paths from route: {routId}, var {routVarId}")
        
        stopResult = findStop.searchByKey(Stop.Keys.ROUTEVARID.value, routVarId).searchByKey(Stop.Keys.ROUTEID.value, routId)
        # print(len(findStop.GetList()))
        curVarSop = stopResult.GetList()[0]
        
        # stopIdNode
        stopIdNode = curVarSop.GetAllStopId()
        
        
        vn = Proj('EPSG:3405')
        
        # stopPoints
        stopCoordLng = curVarSop.GetAllLng()
        stopCoordLat = curVarSop.GetAllLat()
        stopPoints = []
        for i in range(len(stopCoordLng)):
            stopPoints.append(vn(stopCoordLng[i], stopCoordLat[i]))
            
        # pathPoints
        pathResult = findPath.searchByKey(Path.Keys.ROUTEVARID.value, routVarId).searchByKey(Path.Keys.ROUTEID.value, routId)
        # print(len(findPath.GetList()))
        curVarPath = pathResult.GetList()[0]
        pathCoordLng = curVarPath.Getlng()
        pathCoordLat = curVarPath.Getlat()
        pathPoints = []
        for i in range(len(pathCoordLng)):
            pathPoints.append(vn(pathCoordLng[i], pathCoordLat[i]))
        
        graph = createPath(graph, stopIdNode, stopPoints, pathPoints, var.GetRunningTime(), (routId, routVarId))
            
        networkx.is_path(graph, [75, 3210])
            
    
    ug = graph.to_undirected()
    print("Number of subgraphs:", len(list(connected_components(ug))))
    subGraphs = [graph.subgraph(com) for com in list(component for component in list(connected_components(ug)))]
    connectionPair = connectGraph(subGraphs)
    
    for pair in connectionPair:
        graph.add_edge(pair[0], pair[1], time = pair[2]/1.6, dis = pair[2], routeVar = "Walk")
        
    ug = graph.to_undirected()
    
    # print(list(connected_components(ug))[1])
    # for sub in connected_components(ug):
    #     print(ug.subgraph(sub))
    allNode = list(graph.nodes)
    allNode.sort()
    
    
    # print(graph.nodes[35]['coord'])
    # print(graph[7526][7529][0])
    
    return graph
    # print(allNode)

    
if __name__ == "__main__":
    buildGraph()