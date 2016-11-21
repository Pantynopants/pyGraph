# -*- coding=utf-8 -*-
import csv
import networkx as nx
# import matplotlib.pyplot as plt
from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei'] # defult font type 
  
mpl.rcParams['axes.unicode_minus'] = False 

def load_csv_nx(filePath = 'data/graph.csv', start_position = 0, end_position = 1, weight_positon = 2):
    """
    """
    G = nx.Graph()
    # with open(filePath) as f:
    f = open(filePath) 
    
    # f = codecs.open(filePath,'r','utf-8')
    
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

def show(G, path_list = None):
    """
    ref
    ----
    .. [1] https://networkx.github.io/documentation/networkx-1.10/examples/drawing/random_geometric_graph.html
    .. [2] https://networkx.github.io/documentation/networkx-1.10/examples/drawing/labels_and_colors.html
    .. [3] https://networkx.github.io/documentation/networkx-1.10/examples/drawing/weighted_graph.html
    """
    if path_list == None:

        elarge = [(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] > 6]
        esmall = [(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <= 6]
    else:
        elarge = [(u,v) for (u,v,d) in G.edges(data=True)]
        esmall = [ (path_list[i], path_list[i+1])
            for i in range(len(path_list) - 1)
        ]

    pos = nx.spring_layout(G) # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G,pos,node_size = 700)

    # edges
    nx.draw_networkx_edges(G,pos,edgelist = elarge,alpha = 0.5,
                        width = 6)
    nx.draw_networkx_edges(G,pos,edgelist = esmall,
                        width = 6 ,alpha=0.5,edge_color = 'b',style = 'dashed')


    # labels
    nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')

    plt.axis('off')
    # plt.savefig("weighted_graph.png") # save as png
    plt.show() # display
    return