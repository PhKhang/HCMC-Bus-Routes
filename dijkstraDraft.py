
visited = [a]
unvisited = [b, c, d]

dijkstra = [(a, 0), (_, -1), (_, -1), (_, -1)]
while unvisited not empty:
    nodeIdToBranchFrom = visited[-1]
    allNeighbors = [...]
    allNeighbors.remove(i in visited)
        
    for i in dijkstra:
        update
        
    for i in unvisited:
        take the least
        
    unvisited.remove(theLeast)
    visited.append(theLeast)
    
# ------------------------------------------

A

update A with all (v, v) = 0
update A with all edges = weight

for k in nodes:
    for i in nodes:
        for j in nodes:
            if i == j:
                continue
            
            if k == i or k == j:
                continue
            
            if A[i][k] == -1 or A[k][j] == -1:
                continue
            
            if A[i][j] == -1 or A[i][j] > A[i][k] + A[k][j]:
                update = (A[i][k] + A[k][j], k)
    
# ------------------------------------------    
'6885': ('7093', 221.43172040863382),
'7526': (-1, -1),
'7529': (-1, -1),
'7485': (-1, -1),
'7483': (-1, -1),
'7487': (-1, -1),
'7486': (-1, -1),
'7484': (-1, -1),
'7489': (-1, -1),
'7488': (-1, -1),
'7490': (-1, -1),
'7492': (-1, -1),
'7491': (-1, -1),
'7493': (-1, -1),
'7494': (-1, -1),
'7477': (-1, -1),
'7495': (-1, -1),
'7496': (-1, -1),
'7499': (-1, -1),
'7498': (-1, -1),
'7497': (-1, -1),
'7501': (-1, -1),
'7500': (-1, -1),
'7502': (-1, -1),
'7504': (-1, -1),
'7510': (-1, -1),
'7515': (-1, -1),
'7511': (-1, -1),
'7516': (-1, -1),
'7512': (-1, -1),
'7518': (-1, -1),
'7517': (-1, -1),
'7682': (-1, -1),
'7683': (-1, -1),
'7684': (-1, -1),
'7685': (-1, -1),
'7686': (-1, -1)