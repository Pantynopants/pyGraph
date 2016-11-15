# -*- coding=utf-8 -*-
from models import *
from algorithms import dijkstra
import utils
import pandas as pd
import copy 

def CreatTourSortGraph(graph = None):
    """
    para:
        ALGraoh or dataframe
    return: tour route
        list
    """
    if utils.is_graph_type_ALGraph(graph):
        pass
    else:
        dfs_visit = DFSTraverse(graph)
        i = 0
        while i < len(dfs_visit) - 1:
            if is_fin(dfs_visit[:i+2], graph.index):
                return dfs_visit[:i+2]
            if dfs_visit[i+1] not in LocateVex(graph, dfs_visit[i]):
                _, templist = dijkstra(graph, dfs_visit[i], dfs_visit[i+1])
                for insert_poi in templist:                    
                    dfs_visit.insert(i+1, insert_poi)    
                    i += 1     
                
            else:               
                i += 1

        return dfs_visit

def TopoSort(DGlist, graph):
    """
    para: route, with directed; martix
        list, dataframe
    return: circle of route
        list
    """
    # DGlist = list(set(DGlist))
    # print(DGlist)
    # route_martix = graph.loc[DGlist, DGlist]
    # route_martix = route_martix.copy()
    # print(route_martix)
    edarray = EdgesetArray(v = graph.index)
    edarray = edarray.route_to_edgeSetArray(DGlist)
    # temp = edarray.route_to_edgeSetArray(DGlist).get_indegrees()
    # print(temp)

    edge_matrix = edarray.get_all_edges().copy()
    indegree_list = edarray.get_indegrees()
    print(indegree_list)
    stack = []
    for k,v in zip(list(indegree_list.columns.values), indegree_list):
        if v == 0:
            stack.append(k)
    if len(stack) == 0:
        stack.append(u"北门")
    while stack:
        del_poi = stack.pop()
        print("del" + del_poi)
        edarray = edarray.del_vertex(del_poi)
        indegree_list = edarray.get_indegrees()
        print(indegree_list)
        print(edarray.get_all_edges())
        for k,v in zip(list(indegree_list.columns.values), indegree_list):
            if v == 0:
                stack.append(k)
        

########### helper func ###########
def getInDegree(DGlist):
    """
    para:
        list
    return:
        degree_dict = {pointname:point_indegree}
    """
    pass

def DFSTraverse_path(graph, start, goal = None):
    """
    DFS with path as return value
    TODO
    """
    print(graph)
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        print(vertex)
        print(path)
        # new_dict = graph[vertex].pop(path[0])
        for next_key in graph:
            if next_key == goal:
                yield path + [next_key]
            else:
                stack.append((next_key, path + [next_key]))

def DFSTraverse(graph, start_point = u'北门'):
    """
    para:
        graph:DataFrame, start_point:unicode(according to pandas)
    return:
        visited:list
    """
    
    visited = []
    stack = [start_point]
    while stack:
        vertex = stack.pop()
        visited.append(vertex)
        for i in LocateVex(graph, vertex):         
            if i in visited:
                continue
            if i in stack:
                continue
            stack.append(i)
    return visited    


def IsEdge():
    pass

def LocateVex(adjacency_matrix, current_poi):
    """
    para:
        DataFrame, unicode
    return: name(s) of adjacency point of current_poi
        DataFrame
    """
    # start = adjacency_matrix.loc[current_poi]
    return adjacency_matrix[ (adjacency_matrix[current_poi] > 0) & (adjacency_matrix[current_poi] < utils.INF)].index


def is_fin(current_list, view_list):
    """
    check whether the rote of director is finished
    para: viewlist means points you'v visited
        list
    return:
        T if finished
        F if not
    """
    print("*"*100)
    if len(current_list) < len(view_list):
        return False
    for x in view_list:
        if x not in current_list:
            return False
    return True

