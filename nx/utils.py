# -*- coding=utf-8 -*-
import csv
import networkx as nx
# import matplotlib.pyplot as plt
from pylab import *

__all__ = ['load_csv_nx', 'create_nxgraph_from', 'show']

######### for chinese show in matplotlib.pyplot #########

mpl.rcParams['font.sans-serif'] = ['SimHei'] # default font type 
  
mpl.rcParams['axes.unicode_minus'] = False 

def load_csv_nx(file_path = 'data/graph.csv', start_position = 0, end_position = 1, weight_positon = 2):
    """load csv file to networkx.Graph
    Parameters
    -----
    file_path:str
    start_position:int
    end_position:int
    weight_positon:int
        the positon in csv file
        A,B,1 means from A to B, weight is 1
    Returns
    ---------
    networkx.Graph
    """
    G = nx.Graph()
    # with open(file_path) as f:
    f = open(file_path) 
    
    # f = codecs.open(file_path,'r','utf-8')
    
    for line in f:
        if "start" in line:
            continue
        start =  line.strip().split(",")[start_position].decode('utf-8')
        end = line.strip().split(",")[end_position].decode('utf-8')
        weight = line.strip().split(",")[weight_positon].decode('utf-8')
        
        

        G.add_edge(start, end, weight = int(weight))

    return G

def create_nxgraph_from(path_list):
    G = nx.Graph()
    for i in range(len(path_list) - 1):
        G.add_edge(path_list[i], path_list[i+1])
    return G

def show(G, path_list = None, node_list = None):
    """
    Parameters
    -----
    G:networkx.Graph
    path_list:list
        all units are unicode
        [A,B,C,,,]  means from A to B toC
    node_list:list
        all units are unicode
        [A,B,C,,,] means point A B and C
    exapmle
    >>> nxutil.show(g, node_list = circle_path)
    >>> nxutil.show(g, path_list = path)
    ref
    ----
    .. [1] https://networkx.github.io/documentation/networkx-1.10/examples/drawing/random_geometric_graph.html
    .. [2] https://networkx.github.io/documentation/networkx-1.10/examples/drawing/labels_and_colors.html
    .. [3] https://networkx.github.io/documentation/networkx-1.10/examples/drawing/weighted_graph.html
    """
    if path_list == None:

        elarge = [(u,v) for (u,v,d) in G.edges(data=True)]
        # esmall = [(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <= 6]
        esmall = []
    else:
        elarge = [(u,v) for (u,v,d) in G.edges(data=True)]
        if type(path_list[0]) != tuple:
            esmall = [ (str(path_list[i]).encode("utf-8").decode("utf-8"), 
                        str(path_list[i+1]).encode("utf-8").decode("utf-8"))   # [()]
                for i in range(len(path_list) - 1)
            ]
            # print("change")
        else:
            esmall = [ (str(u).encode("utf-8").decode("utf-8"), 
                        str(v).encode("utf-8").decode("utf-8"))   # [()]
                for u,v in path_list
            ]

    pos = nx.spring_layout(G) # positions for all nodes
    # print(pos.keys()[0])
    # print(type(pos.keys()[0]))
    # nodes
    nx.draw_networkx_nodes(G,pos,node_size = 500)
    if node_list != None:
        nx.draw_networkx_nodes(G, pos, nodelist = [val for val in node_list if val in G.nodes()], node_color = 'b', node_size = 600)

    # edges
    nx.draw_networkx_edges(G,pos,edgelist = elarge,alpha = 0.5,
                        width = 6)
    nx.draw_networkx_edges(G,pos,edgelist = esmall,
                        width = 6 ,alpha=0.5,edge_color = 'b',style = 'dashed')


    # labels
    nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')

    plt.axis('off')
    # plt.savefig("Scenic.png") # save as png
    plt.show() # display
    return