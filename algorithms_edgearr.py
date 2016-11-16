# -*- coding=utf-8 -*-
from models import *

def TopoSort(DGlist):
    """
    can not act as a visitor to visit this nodes, to get circle path,
    because it has been confirmed: computer cannot judge the dead loop,
    by Turing
    para: sequent route, with directed; martix
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
    para:
        EdgesetArray
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

    for vertice in graph['vertices']:
        make_set(vertice)

    minimum_spanning_tree = set()
    edges = list(graph['edges'])
    edges.sort()

    for edge in edges:
        weight, vertice1, vertice2 = edge
        if find(vertice1) != find(vertice2):
            union(vertice1, vertice2)
            minimum_spanning_tree.add(edge)
            
    return minimum_spanning_tree