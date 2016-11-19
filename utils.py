# -*- coding=utf-8 -*-
import csv
import numpy as np
import pandas as pd
import re
import json  
import codecs  
import functools
import algorithms
from models import *

INF = 32767

def readFile(filePath = 'data/graph.csv', encoding = "utf-8"):   
    return csv.reader(open(filePath,'r'))   

def writeFile(filePath = 'data/graph.csv', u = None, encoding = "utf-8"):  
    with codecs.open(filePath, "w", encoding) as f:  
        f.write(u) 


def add_dict(thedict, *args): 

    if len(args) == 3:
        if args[0] in thedict:    
            thedict[args[0]].update({args[1]: args[2]})  
        else:
            thedict.update({args[0]:{args[1]: args[2]}})
    elif len(args) == 2:
        if args[0] in thedict:    
            thedict[args[0]].update(args[1])
        else:
            thedict.update({args[0]:args[1]})
        

def debug_print(object, debug = True):
    if debug == True:
        print(object)

def create_matrix(df_index):
    """
    para:index(view name here) of all
        array-like
    return:
        dataframe
    """
    result = pd.DataFrame(INF*np.ones( (len(df_index), len(df_index) ) ), index = df_index, columns = df_index)    
    # point_dict = dict(zip([i for i in range(len(df_index))], df_index))
    for i in df_index:        
        result.set_value(i, i, 0)
    return result

def load_graph(filePath = 'data/graph.csv'):
    """
    do convert from table to matrix without models
    return:
        DataFrame
    """
    df = pd.read_csv(filePath, encoding='utf8', skiprows=0)
    start = list(df['start'])
    end = list(df['end'])
    # print len(start+end)
    point_dict = { i:0
    for i in start+end
    }
    points_list = point_dict.keys()
    # print len(point_dict.keys())
    df_matrix = df.as_matrix()
    # print(result)
    result = create_matrix(points_list)
    for i in df_matrix:
        result.set_value(i[0], i[1], i[2])
        result.set_value(i[1], i[0], i[2])   
    return result


def load_csv_to_models(filePath = 'data/graph.csv'):
    """
    for loop:read the csv 2 times
    because it is undirected graph
    para:
        filePath, absoult or not
    return:
        (headVNode, headArcNode)
    """
    headVNode, headArcNode = VNode(), ArcNode()
    # with open(filePath) as f:
    f = open(filePath) 
    f.next()
# f = codecs.open(filePath,'r','utf-8')
    
    alg = ALGraph()
    # TODO
    for line in f:
        start =  line.strip().split(",")[0].decode('utf-8')
        end = line.strip().split(",")[1].decode('utf-8')
        weight = line.strip().split(",")[2].decode('utf-8')

        pArcNode = ArcNode({end : int(weight)})
        pVNode = VNode(start, pArcNode)
        add_dict(alg, pVNode.name, pVNode.nextArcNode)
        re_pArcNode = ArcNode({start:int(weight)})
        re_pVNode = VNode(end, re_pArcNode)
        add_dict(alg, re_pVNode.name, re_pVNode.nextArcNode)

    # print(len(alg.keys()))
    return alg


# ref: http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/

def ALGraph_to_martix(alg):
    points_list = set([i for i in alg.keys()] + [k for j in alg.values() for k in j.keys()])

    result = pd.DataFrame(INF*np.ones( (len(points_list), len(points_list) ) ), index = points_list, columns = points_list)
    print(result.info())
    for i in points_list:        
        result.set_value(i, i, 0)
    for k,v in alg.items():
        for x,y in v.items():
            result.set_value(k, x, y)
    
    return result

def LocateVex(adjacency_matrix, current_poi):
    """
    para:
        DataFrame, unicode
    return: name(s) of adjacency point of current_poi
        DataFrame
    """
    # start = adjacency_matrix.loc[current_poi]
    return adjacency_matrix[ (adjacency_matrix[current_poi] > 0) & (adjacency_matrix[current_poi] < INF)].index

def graph_type(graph):
    if type(graph) == ALGraph:
        print("ALGraph")
        return "ALGraph", graph
    elif type(graph) == pd.DataFrame:
        print("df matrix")
        return "df", graph

# http://stackoverflow.com/questions/10724854/how-to-do-a-conditional-decorator-in-python-2-6

def get_total_dist(func):
    """deco func: get_total_distance of the list, from a martix
    for those funcs who get df as input and list as output
    """
    @functools.wraps(func)
    def _inner(graph, **kwargs):
        """graph: dataframe
        """
        dis_list = func(graph, **kwargs)
        origin_return = dis_list
        if dis_list == None or len(dis_list) == 0:
            print(" %s wrong return value." % func.__name__)
            return
        if type(dis_list) == tuple:
            dis_list = dis_list[1]
        templist = [] #[(a,b)]
        if type(dis_list[0]) != tuple:
            for i in range(len(dis_list) - 1):
                templist.append( (dis_list[i], dis_list[i+1]) )
        else: templist = dis_list
        # print(templist)
        distance = 0
        for i,j in templist:
            distance += graph.loc[i,j]
        return origin_return, distance
    return _inner


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if (not isinstance(obj, ALGraph) or not isinstance(obj, ArcNode)):
            return super(MyEncoder, self).default(obj)

        return obj.__dict__


if __name__ == '__main__':
    # result, _ = load_graph()
    # 
    temp = load_csv_to_models()
    for k,v in temp.items():
        temp_str = str(k) + ""
        for x,y in v.items():
            temp_str = temp_str + x + y + "\n"
            print(temp_str)
        print("#"*40)

    # print json.dumps(dict(temp), ensure_ascii = False, cls = MyEncoder)
    
            
    result = load_graph()

    print(result)