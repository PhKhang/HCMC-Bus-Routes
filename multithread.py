import asyncio
from concurrent.futures import ProcessPoolExecutor
import networkx
import Graph
from rich.progress import track
import time
import threading
import concurrent.futures

def wok(id, num):
    print('entering cpu_heavy', id, num)
    import time
    time.sleep(2)
    print('leaving cpu_heavy', num)
    return num

async def main(loop, id):
    print('entering main')
    pool = ProcessPoolExecutor(max_workers=10)
    data = await asyncio.gather(*(loop.run_in_executor(pool, wok, id, num) for num in range(5)))
    print('got result', data)
    print('leaving main')


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main(loop, 4))
    
    
# Floyd-Warshall Improved (Multithreading)

calTime = {}

def FloydSubSub(adjArray, nodeList, k, i):
    for j in nodeList:
        if i == j:
            continue
        if k == i or k == j:
            continue
        
        if adjArray[i][k][0] == -1 or adjArray[k][j][0] == -1:
            continue
        
        if adjArray[i][j][0] == -1 or adjArray[i][j][0] > adjArray[i][k][0] + adjArray[k][j][0]:
            adjArray[i][j] = (adjArray[i][k][0] + adjArray[k][j][0], k)

async def FloydSub(loop, adjArray: dict, nodeList, k):
    pool = ProcessPoolExecutor(max_workers=60)
    await asyncio.gather(*(loop.run_in_executor(pool, FloydSubSub, adjArray, nodeList, k, i) for i in nodeList))
    

def FloydWarshall(g: networkx.MultiDiGraph, debug = False):
    start = time.time()
    nodeList = list(g.nodes)
    
    adjArray = {}
    adjArray = {u: {v: (-1, -1) for v in nodeList} for u in nodeList}
    if debug:
        print("Empty adjacent dict in:", time.time() - start)
    start = time.time()
    
    for node in nodeList:
        adjArray[node][node] = (0, node)
        
    edgeList = list(g.edges)
    for u, v, trash in edgeList:
         adjArray[u][v] = (g[u][v][0]['time'], u)
    if debug:
        print("Only intermediate pairs in:", time.time() - start)
         
        
    # return
    nodeL = -1
    longestSoFar = -1
    for k in reversed(nodeList):
        # pool = concurrent.futures.ThreadPoolExecutor(max_workers=60)
        # threadList = []
        if debug:
            print("At", k, end="")
        start = time.time()
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(FloydSub(loop, adjArray, nodeList, k))
        
        # for i in nodeList:
        #     pool.submit(FloydSub, adjArray, nodeList, k, i)
        
        
        # pool.shutdown(wait=True)
        # for thread in threadList:
        #     thread.join()
        
        if debug:
            dur = time.time() - start
            calTime[k] = dur
            if longestSoFar < dur:
                longestSoFar = dur
                nodeL = k
            print(" took:", dur, ", longest so far:", nodeL, "in:", longestSoFar)  
                
    return adjArray

if __name__ == '__main__':
    g = Graph.buildGraph()
    
    print('Starting')
    adj = FloydWarshall(g, True)
