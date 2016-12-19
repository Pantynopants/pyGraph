from models import *
import utils
import pandas as pd
import numpy as np
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

# get all shorest path of the map first
# using ford
# as a matrix, all point are arrivable
# http://python.jobbole.com/81457/
# http://blog.csdn.net/duzuokanyunqi1/article/details/46573429
# https://www.python.org/doc/essays/graphs/
# http://www.python-course.eu/graphs_python.php
# http://tfinley.net/software/pyglpk/ex_ham.html


@utils.get_total_dist
def dfs(graph, start= None, end = None):
    visited = []
    # print(len(graph.columns.values))
    if start == None:
        start = graph.columns.values[0]
    stack = [start]
    while stack:
        vertex = stack.pop()
        if end == vertex and len(visited) >= len(graph.columns.values)-2:
            return visited
        visited.append(vertex)
        for i in utils.LocateVex(graph, vertex):
            
            if i in visited or i in stack:
                continue
            stack.append(i)
    print("faild")
    return visited



# graph = {'A': {'B':1, 'C':2},
#          'B': {'A':1, 'D':2, 'E':3},
#         }

def find_all_paths(graph, start, end, path=[]):
    r"""
    >>> find_all_paths(graph, 'A', 'D')
    [['A', 'B', 'C', 'D'], ['A', 'B', 'D'], ['A', 'C', 'D']]
    """
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return []
    paths = []
    for node in graph[start].keys():
        # print("IN FOR", node)
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def test():
    graph = {'A': {'B':1, 'C':2},
                'B': {'C':1, 'D':2,},
                'C': {'D':5},
                'D': {'C':1},
                'E': {'F':1},
                'F': {'C':1}
            }
    dist = 32767        ##
    min_path = []
    for path in find_all_paths(graph, 'A', 'D'):
        if dist > utils.get_distance(graph, path):
            dist = utils.get_distance(graph, path)
            min_path = path

    print(dist)
    print(min_path)

def TSP(graph, start = None):
    adj_poi_list = utils.LocateVex(graph, start)
    result_path = []
    result_dist = 0

    if len(adj_poi_list) < 2:
        print("bad start point")
        return
    else:
        
        for poi in adj_poi_list:
            print(poi)
            dfs_visit, dist = dfs(graph, start= start, end = poi)

        for i in dfs_visit:
            print(i)
            # print(j)
