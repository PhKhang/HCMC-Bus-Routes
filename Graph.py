import heapq
import json
from math import sqrt
from networkx import connected_components
from pyproj import Proj
from shapely import LineString
from rtree import index
from rich import print
from rich.progress import track
import time
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
                return connectionPair
            
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
        
        # print(f"Making paths from route: {routId}, var {routVarId}")
        
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
            
    
    ug = graph.to_undirected()
    subGraphs = [graph.subgraph(com) for com in list(component for component in list(connected_components(ug)))]
    connectionPair = connectGraph(subGraphs)
    print("Connection pairs:", connectionPair)
    
    # Comment this line to make a full graph
    # return subGraphs[3]
    
    for pair in connectionPair:
        print(pair[0], pair[1], "time = " + str(pair[2]/1.6), "dis = " + str(pair[2]), "routeVar = Walk")
        graph.add_edge(pair[0], pair[1], time = pair[2]/1.6, dis = pair[2], routeVar = "Walk")
        graph.add_edge(pair[1], pair[0], time = pair[2]/1.6, dis = pair[2], routeVar = "Walk")
        
    ug = graph.to_undirected()
    print("Number of subgraphs:", len(list(connected_components(ug))))
    
    allNode = list(graph.nodes)
    allNode.sort()
    
    
    
    return graph

    
# Dijkstra
def Dijkstra(g: networkx.MultiDiGraph, index = 0):
    minHeap = [[0, list(g.nodes)[index], list(g.nodes)[index]]]
    shortestPath = {}
    while len(minHeap) > 0:
        weight, cur, fro = heapq.heappop(minHeap)
        
        if cur in shortestPath:
            continue
        
        shortestPath[cur] = (fro, weight)
        
        for u in networkx.neighbors(g, cur):
            if u not in shortestPath:
                heapq.heappush(minHeap, [weight + g[cur][u][0]['time'], u, cur])
    
    for i in list(g.nodes):
        if i not in shortestPath:
            shortestPath[i] = (-1, -1) 
            
    return shortestPath

def DijkstraOld(k: networkx.MultiDiGraph, startingIndex = 0):
    unvisited = list(k.nodes)
    visited = [unvisited.pop(startingIndex)]
    # unvisited = list(networkx.neighbors(k, visited[-1]))

    if len(list(networkx.neighbors(k, visited[-1]))) == 0:
        # print("No path to any other node found")
        return
        
        
    shortestPath = {}
    for node in list(k.nodes):
        if node == visited[0]:
            shortestPath[node] = (node, 0)
        else:
            shortestPath[node] = (-1, -1)
            
    # print(shortestPath)

    while len(unvisited) > 0:
        nodeToConsider = visited[-1]
        
                
        # Update shortestPath
        for node in unvisited:
            dis = shortestPath[node][1]
            
            # Skip node that cant be reached directly
            if networkx.is_path(k, [nodeToConsider, node]) == False:
                continue
            
            weighToHere = shortestPath[nodeToConsider][1]
            minWeight = k[nodeToConsider][node][0]['time']
            if dis == -1:
                shortestPath[node] = (nodeToConsider, minWeight + weighToHere)
            elif shortestPath[node][1] > minWeight + weighToHere:
                    shortestPath[node] = (nodeToConsider, minWeight + weighToHere)
        
        nextNodeToConsider = -1
        minWeightSoFar = -1
        for u in unvisited:
            # Skip node that are not updated yet
            if shortestPath[u][1] == -1:
                continue
            
            # print(shortestPath[u][1])
            if minWeightSoFar == -1:
                minWeightSoFar = shortestPath[u][1]
                nextNodeToConsider = u
                
            elif shortestPath[u][1] < minWeightSoFar:
                minWeightSoFar = shortestPath[u][1]
                nextNodeToConsider = u
                
        if nextNodeToConsider == -1:
            # print("Unreachable node found")
            return shortestPath
            
        
        # print(shortestPath)
        # print(f"{nextNodeToConsider=}")
        
        unvisited.remove(nextNodeToConsider)
        visited.append(nextNodeToConsider)
        # break

    # print()
    return shortestPath
    
def countImportance(dijkDict: dict, countDict: dict):
    ls = []
    for key in dijkDict:
        heapq.heappush(ls, [len(dijkDict[key]), key])
        
    print(ls)
    
if __name__ == "__main__":
    choice = int(input("1 for starting from scratch, 2 for from file: "))
    
    g = networkx.MultiDiGraph()
    if choice == 1:
        start = time.time()
        g = buildGraph()
        end = time.time()
        print("Graph built in:", end - start)
        
    elif choice == 2:
        g = networkx.read_gml("SavedGraph.bin")
        print(g)
    else:
        print('No choice choosen')
        
    # file = open('shortestPath.json', 'w') 
    allShortestPath = {}
    for node in list(g.nodes):
        allShortestPath[node] = {}
        
    print(networkx.dijkstra_path(g, '35', '7483', weight="time"))
    for i in track(range(len(list(g.nodes))), description = "Running..."):
        start = time.time()
        # print("Starting at:", list(g.nodes)[i])
        
        shortestPath = Dijkstra(g, i)
        
        end = time.time()
        # shortestPath['startingPoint'] = list(g.nodes)[i]
        allShortestPath[list(g.nodes)[i]] = shortestPath
        # print("Calculated in:", end - start)
        
    networkx.write_gml(g, "SavedGraph.bin")
    
    # ug = g.to_undirected()
    # print(len(list(connected_components(ug))))
    
    temp = {}
    # countImportance(allShortestPath, temp)
    print(g)
    # print(allShortestPath['35'])
    
    
    # allNode = list(g.nodes)
    # start = time.time()
    # for i in range(len(allNode)):
    # networkx.single_source_dijkstra_path_length(g, 35, weight="time")
    # print(time.time() - start)