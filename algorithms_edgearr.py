# -*- coding=utf-8 -*-
from models import *
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


def kruskal(graph):
    """
    example return
    >>> minimum_spanning_tree = set([
            ('A', 'B', 1),
            ('B', 'D', 2),
            ('C', 'D', 1),
            ])

    para:
        EdgesetArray
    return:
        set( {()} )
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
 
def prim(G):
    """
    simple input:
    >>>G = {
    ... 0: {1:1, 2:3, 3:4},
    ... 1: {0:1, 2:5},
    ... 2: {0:3, 1:5, 3:2},
    ... 3: {2:2, 0:4}
    ... }
    
    simple output:
    {0: None, 1: 0, 2: 0, 3: 2}
    ---
    para:
        ALGraph
    return:
        dict
    """
    s = G.keys()[0]
    P, Q = {}, [(0, None, s)]
    while Q:
        _, p, u = heappop(Q)
        if u in P: continue
        P[u] = p
        for v, w in G[u].items():
            heappush(Q, (w, u, v)) #weight, predecessor node, node
    return P


 
def kruskal_ALGraph(G):
    """
    simple input:
    >>> G = {
    ... 0: {1:1, 2:3, 3:4},
    ... 1: {2:5},
    ... 2: {3:2},
    ... 3: set()
    ... }
    output:
    >>> print list(kruskal_ALGraph(G)) 
    #[(0, 1), (2, 3), (0, 2)]
    
    para:
        ALGraph
    return:
        set
    """
    def find(C, u):
        if C[u] != u:
            C[u] = find(C, C[u]) # Path compression
        return C[u]
     
    def union(C, R, u, v):
        u, v = find(C, u), find(C, v)
        if R[u] > R[v]: # Union by rank
            C[v] = u
        else:
            C[u] = v
        if R[u] == R[v]: # A tie: Move v up a level
            R[v] += 1
    E = [(G[u][v],u,v) for u in G for v in G[u]]
    T = set()
    C, R = {u:u for u in G}, {u:0 for u in G}   # Comp. reps and ranks
    for _, u, v in sorted(E):
        if find(C, u) != find(C, v):
            T.add((u, v))
            union(C, R, u, v)
    return T
 

