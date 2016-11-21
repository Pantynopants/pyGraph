# -*- coding=utf-8 -*-
from models import *
import utils
import copy
from heapq import heappop, heappush

"""
some algorithms below using models.EdgesetArray
"""

def TopoSort(DGlist):
    """
    can not act as a visitor to visit this nodes, to get circle path,
    because it has been confirmed: computer cannot judge the dead loop,
    by Turing

    para: sequent route, with directed; matrix
        list, dataframe

    return: circle of route
        list
    """
    # DGlist = list(set(DGlist))    
    # route_martix = graph.loc[DGlist, DGlist]
    # route_martix = route_martix.copy()    
    edarray = EdgesetArray(v = list(set(DGlist)) )
    edarray = edarray.route_to_edgeSetArray(DGlist)
    # temp = edarray.route_to_edgeSetArray(DGlist).get_indegrees()    

    # edge_matrix = edarray.get_all_edges().copy()
    indegree_list = edarray.get_indegrees()
    print(indegree_list)
    stack = []
    for k,v in zip(list(indegree_list.columns.values), indegree_list.values[0]):
        if v == 0:
            stack.append(k)
    if len(stack) == 0:
        stack.append(DGlist[0]) # init start point
    del_list = []
    while stack: #O(v*e)
        del_poi = stack.pop()
        print("del" + del_poi)
        # can ont delete twice
        if del_poi in del_list:
            continue
        del_list.append(del_poi)
        edarray = edarray.del_vertex(del_poi)

        indegree_list = edarray.get_indegrees()
        print(indegree_list)
        # print(edarray.get_all_edges().values)
        # map(list,zip(*indegree_list.values))
        for k,v in zip(list(indegree_list.columns.values), indegree_list.values[0]):
            if v == 0:
                stack.append(k)
        # TODO using hash instead of for loop

@utils.not_implemented_for('DataFrame')
def kruskal(graph):
    """
    para:
        EdgesetArray

    return:
        set( {()} )

    example return
    >>> minimum_spanning_tree = set([
            ('A', 'B', 1),
            ('B', 'D', 2),
            ('C', 'D', 1),
            ])

    """
    parent = dict()
    rank = dict()

    def make_set(vertice):
        parent[vertice] = vertice
        rank[vertice] = 0

    def find(vertice):
        if parent[vertice] != vertice:
            parent[vertice] = find(parent[vertice])
        return parent[vertice]

    def union(vertice1, vertice2):
        root1 = find(vertice1)
        root2 = find(vertice2)
        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            else:
                parent[root1] = root2
                if rank[root1] == rank[root2]: rank[root2] += 1

    for vertice in graph.get_all_vertexes():
        make_set(vertice)

    minimum_spanning_tree = set()

    newgraph = copy.deepcopy(graph)
    newgraph = newgraph.sort_weight([u"weight"])
    
    edges = newgraph.as_matrix()

    for edge in edges:
        vertice1, vertice2, weight = edge
        # print(vertice1), 
        # print(vertice2)
        if find(vertice1) != find(vertice2):
            union(vertice1, vertice2)
            minimum_spanning_tree.add((vertice1, vertice2, weight))
            
    return minimum_spanning_tree

"""
some algorithms below using models.ALGraph
"""
 
def prim(graph):
    """
    simple input:
    ```
    >>>graph = {
    ... 0: {1:1, 2:3, 3:4},
    ... 1: {0:1, 2:5},
    ... 2: {0:3, 1:5, 3:2},
    ... 3: {2:2, 0:4}
    ... }
    ```

    simple output:
    ```
    {0: None, 1: 0, 2: 0, 3: 2}
    ```
    ---

    para:
        ALGraph

    return:
        dict
    """
    start = graph.keys()[0]
    result, Q = {}, [(0, None, start)]
    while Q:
        _, p, u = heappop(Q)
        if u in result: continue
        result[u] = p
        for v, w in graph[u].items():
            heappush(Q, (w, u, v)) #weight, predecessor node, node
    return result


 
def kruskal_ALGraph(graph):
    """
    para:
        ALGraph

    return:
        set

    simple input:
    ```
    >>> graph = {
    ... 0: {1:1, 2:3, 3:4},
    ... 1: {2:5},
    ... 2: {3:2},
    ... 3: set()
    ... }
    ```
    output:
    `>>> print list(kruskal_ALGraph(graph)) `
    `#[(0, 1), (2, 3), (0, 2)]    `
    """
    def find(parent, u):
        if parent[u] != u:
            parent[u] = find(parent, parent[u]) # Path compression
        return parent[u]
     
    def union(parent, rank, u, v):
        u, v = find(parent, u), find(parent, v)
        if rank[u] > rank[v]:               # Union by rank
            parent[v] = u
        else:
            parent[u] = v
        if rank[u] == rank[v]:              # Move v up a level
            rank[v] += 1
    E = [(graph[u][v],u,v) for u in graph for v in graph[u]]
    result = set()
    parent, rank = {u:u for u in graph}, {u:0 for u in graph}   # comp. reps and ranks
    for _, u, v in sorted(E):
        if find(parent, u) != find(parent, v):
            result.add((u, v))
            union(parent, rank, u, v)
    return result
 

def bellman_ford(graph, s):
    """
    para
    ------
    graph:ALGraph
    start_poi: unicode

    return
    -------
        dict, dict

    simple use:
    ```
    >>> s, t, x, y, z = range(5)
    >>> W = {
        s: {t:10, y:5},
        t: {x:1, y:2},
        x: {z:4},
        y: {t:3, x:9, z:2},
        z: {x:6, s:7}
        }
    >>> D, P = bellman_ford(W, s)
    >>> print [D[v] for v in [s, t, x, y, z]] # [0, 2, 4, 7, -2]
    >>> print s not in P # True
    >>> print [P[v] for v in [t, x, y, z]] == [x, y, s, t] # True
    ```
    """
    # s = graph.keys().index(s)
    # print(s)
    D, P = {s:0}, {}                           
    for rnd in graph: 

        changed = False                        
        for from_node in graph: 

            for to_node in graph[from_node]: 

                if relax(graph, from_node, to_node, D, P): 

                    changed = True              
        if not changed: break                 
    else:                                     
        raise ValueError('negative cycle')  
    return D, P  

def dijkstra(graph, s):
    """
    para:
        ALGraph, unicode
    return:
        dict, dict

    simple use
    ```
    >>> s, t, x, y, z = range(5)
    >>> W = {
    >>>     s: {t:10, y:5},
    >>>     t: {x:1, y:2},
    >>>     x: {z:4},
    >>>     y: {t:3, x:9, z:2},
    >>>     z: {x:6, s:7}
    >>>     }
    >>> D, P = dijkstra(W, s)
    >>> print [D[v] for v in [s, t, x, y, z]] # [0, 8, 9, 5, 7]
    >>> print s not in P # True
    >>> print [P[v] for v in [t, x, y, z]] == [y, t, s, y] # True
    ```
    """
    D, P, Q, S = {s:0}, {}, [(0,s)], set()   
    while Q:                                 
        _, u = heappop(Q)                       # Node with lowest estimate
        if u in S: continue                     # Already visited
        S.add(u)     
        if u not in graph:
            continue                     # visited it
        for v in graph[u]: 
                                     # Go through all its neighbors
            relax(graph, u, v, D, P)                # Relax the out-edge
            heappush(Q, (D[v], v))             
    return D, P 

def johnson(graph):    
    """
    johnson: combine Bellman-Ford with Dijkstra
    solve all point's short path  in graph
    perform well in sparse graph
    complexity : O(mnlgn) 

    para
    -----
    graph:ALGraph

    return
    --------
    dict{dict{}}, dict{dict{}}

    simple use:
    ```
    >>> a, b, c, d, e = range(5)
    >>> W = {
        a: {c:1, d:7},
        b: {a:4},
        c: {b:-5, e:2},
        d: {c:6},
        e: {a:3, b:8, d:-4}
        }
    >>> D, P = johnson(W)
    >>> print [D[a][v] for v in [a, b, c, d, e]] # [0, -4, 1, -1, 3]
    >>> print [D[b][v] for v in [a, b, c, d, e]] # [4, 0, 5, 3, 7]
    >>> print [D[c][v] for v in [a, b, c, d, e]] # [-1, -5, 0, -2, 2]
    >>> print [D[d][v] for v in [a, b, c, d, e]] # [5, 1, 6, 0, 8]
    >>> print [D[e][v] for v in [a, b, c, d, e]] # [1, -3, 2, -4, 0]
    ```
    """
    graph = copy.deepcopy(graph)                           
    s = graph.keys()[0]  
    print("#"*40) 
    print(s)                           
    graph[s] = {v:0 for v in graph}             
    h, _ = bellman_ford(graph, s)                   # h[v]: Shortest dist from s
    del graph[s]                               
    for u in graph:                                 # The weigraphht from u...
        for v in graph[u]:                          # from u to v...
            graph[u][v] += h[u] - h[v]        
    D, P = {}, {}                             
    for u in graph:                           
        D[u], P[u] = dijkstra(graph, u)             # ... find the shortest paths
        for v in graph:                             # For each destination...
            D[u][v] += h[v] - h[u]              # ... readjust the distance
    return D, P  

def floyd_warshall1(graph):
    """
    para
    ------
    graph: ALGraph

    return
    -------
        dict{dict{}}

    simple use:
    ```
    >>> a, b, c, d, e = range(1,6) # One-based
    >>> W = {
    >>>     a: {c:1, d:7},
    >>>     b: {a:4},
    >>>     c: {b:-5, e:2},
    >>>     d: {c:6},
    >>>     e: {a:3, b:8, d:-4}
    >>>     }
    >>> for u in W:
    >>>     for v in W:
    >>>         if u == v: W[u][v] = 0
    >>>         if v not in W[u]: W[u][v] = utils.INF
    >>> D = floyd_warshall1(W)
    >>> print [D[a][v] for v in [a, b, c, d, e]] # [0, -4, 1, -1, 3]
    >>> print [D[b][v] for v in [a, b, c, d, e]] # [4, 0, 5, 3, 7]
    >>> print [D[c][v] for v in [a, b, c, d, e]] # [-1, -5, 0, -2, 2]
    >>> print [D[d][v] for v in [a, b, c, d, e]] # [5, 1, 6, 0, 8]
    >>> print [D[e][v] for v in [a, b, c, d, e]] # [1, -3, 2, -4, 0]
    ```
    """
    distance = copy.deepcopy(graph)                           
    for k in distance:                               
        for u in distance:
            for v in distance:
                a, b = 0,0
                try:
                    a = distance[u][v]                    
                except :
                    a = utils.INF
                try:
                    b = distance[u][k] + distance[k][v]
                except :
                    b = utils.INF
                else:
                    utils.add_dict(distance, u, v, min(a,b))               
    return distance

################# helper func #################

def relax(W, u, v, D, P):
    """
    reference
    ----------
    .. [1] http://python.jobbole.com/81467/
    """
    # print (W[u][v].encode('utf-8'))
    # print type(D.get(u, utils.INF))
    d = D.get(u, utils.INF) + int(W[u][v])
    if d < D.get(v, utils.INF):                       
        D[v], P[v] = d, u                      
        return True 