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

def DFSTraverse(_graph, start, end = None):
    graph = copy.deepcopy(_graph)
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))

def IsEdge():
    pass

def LocateVex():
    pass

def FindInDegree():
    pass

# if __name__ == '__main__':
#     graph = load_graph()
#     CreatTourSortGraph()