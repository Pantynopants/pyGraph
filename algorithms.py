# -*- coding=utf-8 -*-

import utils
import copy
import pandas as pd  
import heapq

from models import *

"""
all algorithms in this model receive Pandas.DataFrame as input
"""
# tutorial http://stackoverflow.com/questions/22897209/dijkstras-algorithm-in-python
# http://www.cnblogs.com/biyeymyhjob/archive/2012/07/31/2615833.html

# @utils.get_total_dist
def dijkstra(graph, start = None, end = None):
    """
    # TODO: change to ndarray
    para:
        DataFrame, str(unicode), str(unicode)
    return:distance from start to every point; the path from start point to others
        dist = {
        pointName:( distance = graph[start] (dataframe), isVisted = 0, path = [] )
        }
        or
        distance:number, path:list
    """    
    # dist:distance from start point to others
    # dist = {
    #   pointName:( distance = graph[start] (dataframe), isVisted = 0, path = [] )
    # }
    if start == None:
        print("wrong input: plz input a start point")
        return
    dis = zip(graph[start].index, graph[start])
    dist = {
        k:[v, 0, []]
        for k,v in dis            
    }
    for i in range(len(graph.index) - 1):
        mindis = utils.INF
        add_point = ""
        for k,v in dist.items():
            if v[1] == 0 and v[0] < mindis and v[0] > 0:
                mindis = v[0]
                add_point = k
        dist[add_point][1] = 1 # mark as visited
        for column_df_index in graph[add_point].index:
            
            if (graph.at[add_point, column_df_index] < utils.INF) and (dist[column_df_index][1] == 0):
                # print( (str(graph.at[add_point, column_df_index] + dist[add_point][0]) ) + "\t" + str(dist[column_df_index][0]))
                if dist[column_df_index][0] > graph.at[add_point, column_df_index] + dist[add_point][0]:
                    dist[column_df_index][0] =  graph.at[add_point, column_df_index] + dist[add_point][0]                    
                    dist[column_df_index][2].extend(dist[add_point][2]) 
                    dist[column_df_index][2].append(add_point) 
                    # print(len(dist[column_df_index][2]))

    path = []
    for k,v in dist.items():
        temp_str = []
        temp_str.extend([x for x in v[2]])
        temp_str.extend([v[0], k])
        path.append(temp_str)    

    if end == None:        
        return dist, path
    else:
        return dist[end][0], dist[end][2]
    

def floyd(graph):
    """
    let all points' edges to simplified
    para:
        pd.dataframe
    return:
        pd.dataframe
    """
    result = graph.copy()
    points_list = result.index.tolist()
    point_dict = dict(zip([i for i in range(len(points_list))], points_list))
    
    result_matrix = result.as_matrix()
    # Floyd-Warshall algorithm
    for k in range(len(result_matrix)):
        for i in range(len(result_matrix)):
            for j in range(len(result_matrix)):
                if(result_matrix[i][k] < utils.INF and result_matrix[k][j] < utils.INF and result_matrix[i][j] > result_matrix[i][k] + result_matrix[k][j]):
                    
                    result.set_value(point_dict[i], point_dict[j], result_matrix[i][k] + result_matrix[k][j])
                    result.set_value(point_dict[j], point_dict[i], result_matrix[i][k] + result_matrix[k][j])

                    result_matrix[i][j] = result_matrix[i][k] + result_matrix[k][j] 
    return result


def MST(graph, method = "prim_heap"):
    if method == "prim_heap":
        return prim_heap(graph)
    
@utils.get_total_dist
def prim_heap(graph): 
    """
    using heap to optimtiz algorithm
    para:
        dataframe
    return: a list of MST
        list
    """
    n = len(graph )

    # vertexes = [u"北门"]
    vertexes = [graph.index[0]]

    edges = {}
    total_v = set(graph.index) #{}
    
    def get_heap(unicode_v):
        """return: (weight, target_poi, from_poi)
        """
        return [ (w, v, unicode_v) 
            for w,v in zip(graph[unicode_v], graph[unicode_v].index) 
            if 0 < w < utils.INF and v != unicode_v]

    heap = get_heap(list(vertexes)[0])
    heapq.heapify(heap)
    # print heapq.nlargest(1, heap, key = lambda x:x[1])
    edge_list = []
    while len(vertexes) != n:
        # get min weight edge in graph in <u,v>, u in vertexes and v is not
        # next_w_v = heapq.nsmallest(1, heap, key = lambda x:x[1]) #[(w,v)]
        next_w_v = heapq.heappop(heap) #pop it. the min edge use only once
        print(next_w_v[1])
        if next_w_v[1] in vertexes:
            continue                        
        
        vertexes.append(next_w_v[1])
        edge_list.append( (next_w_v[2], next_w_v[1]) )
        for w,v,f in get_heap(next_w_v[1]):
            if v not in vertexes:                
                heapq.heappush(heap, (w,v,f) )
        
    return edge_list                        

def prim(graph):
    n = len(graph)    
    dis = [0]*n  
    pre = [0]*n  
    flag = [False]*n  
    flag[0] = True  
    k = 0  
    for i in range(n):  
        dis[i] = graph[k][i]  
    for j in range(n-1):  
        mini = utils.INF
        for i in range(n):  
            if mini > dis[i] and not flag[i]:  
                mini = dis[i]  
                k = i  
        if k == 0: # graph not connected 
            print("graph not connected ")
            return 
        flag[k] = True  
        for i in range(n):  
            if dis[i] > graph[k][i] and not flag[i]:  
                dis[i] = graph[k][i]  
                pre[i] = k  
    print(dis)  
    print(pre)
    return (dis, pre)

# ref https://github.com/israelst/Algorithms-Book--Python

def DFSTraverse_path(graph, start, goal = None):
    """
    DFS with path as return value
    iterable.
    para:
        graph:DataFrame, start:unicode(according to pandas)
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


@utils.get_total_dist
def DFSTraverse(graph, start = None):
    """
    para:
        graph:DataFrame, start:unicode(according to pandas)
    return:
        visited(list), path(list [(a,b),(b,c),,,]): real road, consecutive
    """
    
    visited = []
    stack = [start]
    while stack:
        vertex = stack.pop()
        visited.append(vertex)
        for i in utils.LocateVex(graph, vertex):         
            if i in visited or i in stack:
                continue
            stack.append(i)
    # finish dfs       
    # get path of DFS
    path = []
    for i in range(len(visited) - 1):
        if graph.loc[visited[i], visited[i+1]] == utils.INF:
            for j in range(i+1):
                if graph.loc[visited[j], visited[i+1]] != utils.INF:
                    path.append( (visited[j], visited[i+1]) )
                    break
        elif graph.loc[visited[i], visited[i+1]] != 0:
            path.append( (visited[i], visited[i+1]) )

    return visited, path

