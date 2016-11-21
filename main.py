# -*- coding=utf-8 -*-
from Vgraph import director, parking, recommend
from models import *
import utils
import algorithms
import algorithms_edgearr
import nx
import sys
import os
reload(sys)
sys.setdefaultencoding( "utf-8" )

def main():
    # director.CreatTourSortGraph(ALGraph())
    # temp = utils.load_csv_to_models() #ALGraph
    # print(temp)
    # print("#"*40)
    # distance = 0
    temp = utils.load_graph() #dataframe
    # temp = utils.load_graph(filePath = 'data/topo3.csv',
    # start_position = 1, end_position = 2, weight_positon = 3)
    # temp = temp[u"北门"]

    # for i in temp.index.index:
    #     print(i)
    # algorithms.floyd(temp)

    path, distance = director.CreatTourSortGraph(temp) 
    print("#"*40)
    for i in path:
        print(i)
    print("#"*40)   
    g = nx.utils.load_csv_nx()
    # nx.utils.show(g)
    # p = nx.utils.create_nxgraph_from(path)
    nx.utils.show(g, path_list = path)


    # algorithms_edgearr.TopoSort(path)


    # dis_list, distance = algorithms.MST(temp)
    # for x in dis_list:
    #      print(x)
    # print(distance)


    # points, distance = director.DFSTraverse(temp, start = u'北门') 
    # for i in path:
    #     print(i)
    # print("#"*40)


    # path, dist = algorithms.dijkstra(temp,  start = u'北门')
    # for x in path:
    #     for y in x:
    #         print(y)
    #     print("\n")

    # temp = EdgesetArray()
    # temp = temp.load_csv()
    # tree = algorithms_edgearr.kruskal(temp)
    # for x in tree:
    #     print(x[0]),
    #     print(x[1]),
    #     print(x[2])
    
    # path = algorithms_edgearr.prim(temp)
    # for i,j in path.items():
    #     print(i), 
    #     print(j)

    # for i,j in algorithms_edgearr.kruskal_ALGraph(temp):
    #     print(i), 
    #     print(j)
    
    # D, P = algorithms_edgearr.bellman_ford(temp, u"北门")
    # print(D)
    # for k,v in D.items():
    #     print(k), 
    #     print(v)

    # path, _ = algorithms_edgearr.dijkstra(temp, u"北门")
    # print(type(path))
    # for i,j in path.items():
    #     print(i),
    #     print(j)

    # D, P = algorithms_edgearr.johnson(temp)
    # for k,v in D.items():
    #     for x,y in v.items():
    #         print(k),
    #         print(x),
    #         print(y)

    # D = algorithms_edgearr.floyd_warshall1(temp)
    # for k,v in D.items():
    #     for x,y in v.items():
    #         print(k),
    #         print(x),
    #         print(y)
    print("total distance:"),
    print(distance)

def start():
    print("welcome to tourism management system")
    print("plz enter a number:")
    print("1. input Scenic Spots graph")
    print("2. show Scenic Spots graph")
    print("3. show Tour guide Graph")
    print("4. show circle road in guide Graph")
    print("5. calculate shortest path and distance")
    print("6. show road constraction plan")
    print("7. search and sort Scenic Spots")
    print("8. parking system")
    print("0. exit")
    while True:       
        line = raw_input("enter sth, seperate by space")
        if int(line.strip()[0]) == 0:
            break
        flag = False
        g = None
        path = None
        temp = utils.load_graph() #dataframe
        # temp = utils.load_graph(filePath = 'data/topo3.csv',
        # start_position = 1, end_position = 2, weight_positon = 3)

        if line.strip() == "1":
            director.input_TourSortGraph()
            flag = True
            temp = utils.load_graph(filePath = 'data/graph1.csv',
        start_position = 0, end_position = 1, weight_positon = 2)

        elif line.strip() == "2":
            if flag:
                g = nx.utils.load_csv_nx('data/graph1.csv')
            else: g = nx.utils.load_csv_nx()
            nx.utils.show(g)
        elif line.strip() == "3":
            path, distance = director.CreatTourSortGraph(temp) 
            print("#"*40)
            for i in path:
                print(i)
            print("#"*40)   
            if g == None:
                g = nx.utils.load_csv_nx()
            nx.utils.show(g, path_list = path)
        elif line.strip() == "4":
            if path == None:
                print("plz show Tour guide Graph first, now input 3")
                continue
            algorithms_edgearr.TopoSort(path)
        elif line.strip() == "5":
            poi = raw_input("enter startpoint and endpoint, input -1 for a defult value")
            if len(poi.strip().split()) != 1:
                shortest_path, dist = algorithms.dijkstra(temp,  start = poi.split()[0], end = poi.split()[1])
            else:
                shortest_path, dist = algorithms.dijkstra(temp,  start = u'北门', end = u'碧水亭')
            # for x in shortest_path:
            #     for y in x:
            #         print(y)
            #     print("\n")
        elif line.strip() == "6":
            dis_list, distance = algorithms.MST(temp)
            for x in dis_list:
                 print(x)
            print(distance)
        elif line.strip() == "7":
            recommend.start()
        elif line.strip() == "8":
            parking.start()



if __name__ == '__main__':
    start()
    # main()
    # parking.start()
    # recommend.start()
    # g = nx.utils.load_csv_nx(filePath = 'data/topo3.csv', start_position = 1, end_position = 2, weight_positon = 3)
    # g = nx.utils.load_csv_nx()
    # nx.utils.show(g)
