# -*- coding=utf-8 -*-
import csv
import numpy as np
import pandas as pd
import re
import json  
import codecs  
import algorithms
from models import *

INF = 32767

def readFile(filePath = 'graph.csv', encoding = "utf-8"):   
    return csv.reader(open(filePath,'r'))   

def writeFile(filePath = 'graph.csv', u = None, encoding = "utf-8"):  
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

def load_graph(filePath = 'graph.csv'):
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


def load_csv_to_models(filePath = 'graph.csv'):
    """
    for loop:read the csv 2 times
    because it is undirected graph
    para:
        filePath, absoult or not
    return:
        (headVNode, headArcNode)
    """
    headVNode, headArcNode = VNode(), ArcNode()
    
    f = readFile()
    f.next()
    alg = ALGraph()
    
    for line in f:
        pArcNode = ArcNode({line[1]:line[2]})
        pVNode = VNode(line[0], pArcNode)
        add_dict(alg, pVNode.name, pVNode.nextArcNode)
        re_pArcNode = ArcNode({line[0]:line[2]})
        re_pVNode = VNode(line[1], re_pArcNode)
        add_dict(alg, re_pVNode.name, re_pVNode.nextArcNode)

    print(len(alg.keys()))
    return alg


# http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
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


def is_graph_type_ALGraph(graph):
    if type(graph) == ALGraph:
        print("ALGraph")
        return True
    elif type(graph) == pd.DataFrame:
        print("df martix")
        return False


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if (not isinstance(obj, ALGraph) or not isinstance(obj, ArcNode)):
            return super(MyEncoder, self).default(obj)

        return obj.__dict__


# def process_graph(graph, *func = [print()]):
#     for k,v in graph.items():
#         # if v is not None:func(k),
#         for x,y in v.items():
#             func(x),
#             func(y)

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