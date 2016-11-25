# -*- coding=utf-8 -*-
from __future__ import nested_scopes
import new

import csv
import numpy as np
import pandas as pd
import re
import json  
import codecs  
import functools
from decorator import decorator

import models

INF = 32767
PRINT_DEBUG = True

def readFile(file_path = 'data/graph.csv', encoding = "utf-8"):   
    return csv.reader(open(file_path,'r'))   

def writeFile(file_path = 'data/graph.csv', u = None, encoding = "utf-8"):  
    with codecs.open(file_path, "w", encoding) as f:  
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
        

def debug_print(object, debug = PRINT_DEBUG):
    """control by global variable
    debug = PRINT_DEBUG
    """
    if debug == True:
        print(object)




def enhance_method(target_class, method_name, replacement):
    """
    replace exist methods
    if u want to change a function in class, using it

    para
    -----
    target_class: str(class name)
    method_name: str
    replacement: pointer to function

    ref
    ----
    .. [1] http://outofmemory.cn/code-snippet/2856/python-dongtai-modify-class-method-execution-logical
    """
    method = getattr(target_class, method_name)
    setattr(target_class, method_name, new.instancemethod(
        lambda *args, **kwds: replacement(method, *args, **kwds), None, target_class))


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

def load_graph(file_path = 'data/graph.csv',
    start_position = 0, end_position = 1, weight_positon = 2):
    """
    do convert from table to matrix without models
    start_position:int
    end_position:int
    weight_positon:int
        the positon in csv file
        A,B,1 means from A to B, weight is 1
    return:
        DataFrame
    """
    df = pd.read_csv(file_path, encoding='utf8', skiprows=0)
    start = list(df['start'])
    end = list(df['end'])
    point_dict = { i:0
    for i in start+end
    }
    points_list = point_dict.keys()

    df_matrix = df.as_matrix()

    result = create_matrix(points_list)
    for i in df_matrix:
        result.set_value(i[start_position], i[end_position], i[weight_positon])
        result.set_value(i[end_position], i[start_position], i[weight_positon])   
    return result


def load_csv_to_models(file_path = 'data/graph.csv',
    start_position = 0, end_position = 1, weight_positon = 2, 
    vnode = "models.VNode", arcnode = "models.ArcNode", 
    algraph = "models.ALGraph" ):
    """
    load csv file, with: start, end, weight; format
    to VNode, ArcNode, ALGraph

    for loop:read the csv 2 times
    because it is undirected graph

    para
    ------
        file_path(absoult or not):str
        vnode:str(class name, for creating class dynamic)
        arcnode:str
        algraph:str
        start_position:int
        end_position:int
        weight_positon:int
            the positon in csv file
            A,B,1 means from A to B, weight is 1
    return
    -------
        algraph: (models.ALGraph by default)
    """

    f = open(file_path) 
    # f.next()

    
    alg = eval(algraph)()
    for line in f:
        if "start" in line:
            continue
        start =  line.strip().split(",")[0].decode('utf-8')
        end = line.strip().split(",")[1].decode('utf-8')
        weight = line.strip().split(",")[2].decode('utf-8')        

        pArcNode = eval(arcnode)({end : int(weight)})
        pVNode = eval(vnode)(start, pArcNode)
        add_dict(alg, pVNode.name, pVNode.nextArcNode)
        re_pArcNode = eval(arcnode)({start:int(weight)})      # for undigraph, load twice
        re_pVNode = eval(vnode)(end, re_pArcNode)
        add_dict(alg, re_pVNode.name, re_pVNode.nextArcNode)

    # print(len(alg.keys()))
    return alg



def ALGraph_to_martix(alg):
    """
    para
    ------
    alg:ALGraph

    return
    ------
    result:DataFrame
    """
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
    if type(graph) == models.ALGraph:
        print("ALGraph")
        return "ALGraph", graph
    elif type(graph) == pd.DataFrame:
        print("df matrix")
        return "df", graph

################### decorator #########################


def get_total_dist(func):
    """deco func: get_total_distance of the list, from a martix
    for those funcs who get df as input and list as output
    
    return
    -------
    origin_return, distance:int
    
    ref
    ---
    .. [1] http://stackoverflow.com/questions/10724854/how-to-do-a-conditional-decorator-in-python-2-6
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
        if len(dis_list)>0 and type(dis_list[0]) != tuple:
            for i in range(len(dis_list) - 1):
                templist.append( (dis_list[i], dis_list[i+1]) )
        else: templist = dis_list
        # print(templist)
        distance = 0
        for i,j in templist:
            distance += graph.loc[i,j]
        return origin_return, distance
    return _inner

def not_implemented_for(*graph_types):
    """Decorator to mark algorithms as not implemented
    Parameters
    ----------
    graph_types : container of strings
        Entries must be one of 'directed','undirected', 'multigraph', 'graph'.
    Returns
    -------
    _require : function
        The decorated function.
    Raises
    ------
    KeyError
    Notes
    -----
    Multiple types are joined logically with "and".
    For "or" use multiple @not_implemented_for() lines.
    Examples
    --------
    Decorate functions like this::
       @not_implemnted_for('directed')
       def sp_function(G):
           pass
       @not_implemnted_for('directed','multigraph')
       def sp_np_function(G):
           pass

    ref
    ----
    .. [1] https://github.com/networkx/networkx/blob/6e20b952a957af820990f68d9237609198088816/networkx/utils/decorators.py#L16
    """
    @decorator
    def _not_implemented_for(f, *args, **kwargs):
        graph = args[0]

        terms = {
        'ALGraph':type(graph) == models.ALGraph,
        'DataFrame':type(graph) == pd.DataFrame,
        'EdgesetArray':type(graph) == models.EdgesetArray
        }
        match = True
        try:
            for t in graph_types:
                match = match and terms[t]
        except KeyError:
            raise KeyError('use one or more of ',
                           'directed, undirected, multigraph, graph')
        if match:
            print('not implemented for %s type'%
                                            ' '.join(graph_types))
            return 
        else:
            return f(*args,**kwargs)
    return _not_implemented_for


class MyEncoder(json.JSONEncoder):
    """using JSON to save graph data
    #TODO
    """
    def default(self, obj):
        if (not isinstance(obj, ALGraph) or not isinstance(obj, models.ArcNode)):
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