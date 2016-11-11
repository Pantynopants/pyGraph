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
def DFSTraverse(graph, start_point = '北门'):
    # visited, stack = set(start), [start]
    # while stack:
    #     vertex = stack.pop()
    #     if vertex not in visited:
    #         visited.add(vertex)
    #         stack.extend(graph[vertex].pop(visited))
    # return visited
    print(graph.index)
    start = graph.loc[unicode(start_point, "utf-8")]
    print(graph.loc[])
    return start
    # print (graph[graph.'北门' > 0 & graph.'北门' < 32767])


def IsEdge():
    pass

def LocateVex():
    pass

def FindInDegree():
    pass

# if __name__ == '__main__':
#     graph = load_graph()
#     CreatTourSortGraph()