# -*- coding=utf-8 -*-
from models import *
import utils
import pandas as pd
import copy 

def CreatTourSortGraph(graph = None):
    if utils.is_graph_type_ALGraph(graph):
        pass
    else:
        pass

def TopoSort():
    pass
########### helper func ###########

def DFSTraverse_path(graph, start, goal = None):
    """
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

    # visited, stack = set(start), [start]
    # while stack:
    #     vertex = stack.pop()
    #     if vertex not in visited:
    #         visited.add(vertex)
    #         stack.extend(graph[vertex].pop(visited))
    # return visited
    # print(graph.index)
    # print(LocateVex(graph, start_point))
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
    # print (graph[graph.'北门' > 0 & graph.'北门' < 32767])


def IsEdge():
    pass

def LocateVex(adjacency_matrix, current_poi):
    """
    para:
        DataFrame, str
    return: name(s) of adjacency of current_poi
        DataFrame
    """
    start = adjacency_matrix.loc[current_poi]
    x = adjacency_matrix[ (adjacency_matrix[current_poi] > 0) & (adjacency_matrix[current_poi] < 32767)]

    return x.index

def FindInDegree():
    pass

# if __name__ == '__main__':
#     graph = load_graph()
#     CreatTourSortGraph()