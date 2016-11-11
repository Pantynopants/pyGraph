# -*- coding=utf-8 -*-
import csv
import numpy as np
import pandas as pd
import re
import json  
from models import *

import codecs  
  
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

INF = 32767
# do convert from table to matrix without models
def load_graph(filePath = 'graph.csv'):
    
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
    result = pd.DataFrame(32767*np.ones( (len(points_list), len(points_list) ) ), index = points_list, columns = points_list)
    
    point_dict = dict(zip([i for i in range(len(points_list))], points_list))
    for i in points_list:        
        result.set_value(i, i, 0)
    for i in df_matrix:
        result.set_value(i[0], i[1], i[2])
        result.set_value(i[1], i[0], i[2])

    result, result_matrix = Floyd_algorithm(result)

    return result, result_matrix

def Floyd_algorithm(result):
    """
    para:
        pd.dataframe
    return:
        pd.dataframe, martix(list(list))
    """
    points_list = result.index.tolist()
    point_dict = dict(zip([i for i in range(len(points_list))], points_list))
    
    result_matrix = result.as_matrix()
    # Floyd-Warshall algorithm
    for k in range(len(result_matrix)):
        for i in range(len(result_matrix)):
            for j in range(len(result_matrix)):
                if(result_matrix[i][k] < INF and result_matrix[k][j] < INF and result_matrix[i][j] > result_matrix[i][k] + result_matrix[k][j]):
                    
                    result.set_value(point_dict[i], point_dict[j], result_matrix[i][k] + result_matrix[k][j])
                    result.set_value(point_dict[j], point_dict[i], result_matrix[i][k] + result_matrix[k][j])

                    result_matrix[i][j] = result_matrix[i][k] + result_matrix[k][j] 
    return result, result_matrix


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
        re_pVNode = VNode(line[1], pArcNode)
        add_dict(alg, re_pVNode.name, re_pVNode.nextArcNode)

    print(len(alg.keys()))
    return alg
# http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
def ALGraph_to_martix(alg):
    points_list = set([i for i in alg.keys()] + [k for j in alg.values() for k in j.keys()])

    result = pd.DataFrame(INF*np.ones( (len(points_list), len(points_list) ) ), index = points_list, columns = points_list, encoding='utf-8')
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

def process_graph(graph, *func = [print()]):
    for k,v in graph.items():
        # if v is not None:func(k),
        for x,y in v.items():
            func(x),
            func(y)

if __name__ == '__main__':
    # result, _ = load_graph()
    # 
    temp = load_csv_to_models()
    process_graph(temp)
    print json.dumps(dict(temp), ensure_ascii = False, cls = MyEncoder)
    # for x in temp:
    #     for y in x.nextArcNode:
    #         print(x.name, y.endViewName, y.weight)
            
    # result, _ = Floyd_algorithm(ALGraph_to_martix(temp))

    # print(result)