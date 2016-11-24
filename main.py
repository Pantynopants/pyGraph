# -*- coding=utf-8 -*-
from Vgraph import director, parking, recommend
from models import *
import utils
import algorithms
import algorithms_edgearr
from nx import utils as nxutil
import sys
import os
# import chardet
import datetime

reload(sys)
sys.setdefaultencoding( "utf-8" )

def main():
    # director.CreatTourSortGraph(ALGraph())
    # temp = utils.load_csv_to_models() #ALGraph
    # print(temp)
    # print("#"*40)
    distance = 0
    temp = utils.load_graph() #dataframe
    # temp = utils.load_graph(file_path = 'data/topo3.csv',
    # start_position = 1, end_position = 2, weight_positon = 3)
    # temp = temp[u"北门"]

    # for i in temp.index.index:
    #     print(i)
    # algorithms.floyd(temp)

    # path, distance = director.CreatTourSortGraph(temp) 
    # print("#"*40)
    # for i in path:
    #     print(i)
    # print("#"*40)   
    # g = nxutil.load_csv_nx()
    # # nxutil.show(g)
    # # p = nxutil.create_nxgraph_from(path)
    # nxutil.show(g, path_list = path)


    # algorithms_edgearr.TopoSort(path)


    # dis_list, distance = algorithms.MST(temp)
    # for x in dis_list:
    #      print(x)
    # print(distance)


    # (points, path), distance = algorithms.DFSTraverse(temp, start = u'北门') 
    # for i,j in path:
    #     print(i),
    #     print(j)
    # print("#"*40)


    # dist, path = algorithms.dijkstra(temp,  start = u'碧水亭', end = u"北门")
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

def compare():
    df = utils.load_graph(file_path = 'data/topo4.csv',
        start_position = 1, end_position = 2, weight_positon = 3)
    alg = utils.load_csv_to_models(file_path = 'data/topo4.csv',
        start_position = 1, end_position = 2, weight_positon = 3)

    df1 = utils.load_graph(file_path = 'data/topo2.csv',
                start_position = 1, end_position = 2, weight_positon = 3)
    alg1 = utils.load_csv_to_models(file_path = 'data/topo2.csv',
                start_position = 1, end_position = 2, weight_positon = 3)


    while True:       
        print("'dfs' for dfs and bsf traverse")
        print("'dij' for dijkstra")
        print("'ford' for ford algorithm")
        print("'johnson' for johnson algorithm")
        print("'prim' for prim algorithm")
        print("'kruskal' for kruskal algorithm")
        print("'topo' for toposort")

        line = raw_input("input function name to start compare, 0 to exit\n")
        

        if line.strip() == "0":
            break
        elif line.strip() == "dfs":
            print(algorithms.BFSTraverse.__doc__)
            ########### dfs bfs ##############
            print("DataFrame for bfs and dfs")
            print(get_func_time(algorithms.BFSTraverse, df))
            print(get_func_time(algorithms.DFSTraverse, df))
            print("ALGraph for bfs and dfs")
            print(get_func_time(algorithms_edgearr.BFSTraverse, alg))
            print(get_func_time(algorithms_edgearr.DFSTraverse, alg))

        elif line.strip() == "dij":
            print(algorithms.dijkstra.__doc__)
            ########### dijkstra ##############
            print("DataFrame for dijkstra")
            print(get_func_time(algorithms.dijkstra, df))
            print("ALGraph for dijkstra")
            print(get_func_time(algorithms_edgearr.dijkstra, alg))

        elif line.strip() == "ford":
            print(algorithms.floyd.__doc__)
            ########### ford ############## 
            print("DataFrame for floyd")        
            print(get_func_time(algorithms.floyd, df1))
            print("ALGraph for bellman_ford")   
            print(get_func_time(algorithms_edgearr.bellman_ford, alg1))
            print("ALGraph for floyd_warshall1")   
            print(get_func_time(algorithms_edgearr.floyd_warshall1, alg1))

        elif line.strip() == "johnson":
            print(algorithms_edgearr.johnson.__doc__)
            ########### johnson ###########
            print("ALGraph for johnson")
            print(get_func_time(algorithms_edgearr.johnson, alg))

        elif line.strip() == "prim":
            print(algorithms_edgearr.prim.__doc__)
            ########### prim ###########  
            print("DataFrame for prim")      
            print(get_func_time(algorithms.prim, df))
            print("DataFrame for prim using heap to speed up")    
            print(get_func_time(algorithms.prim_heap, df))
            print("ALGraph for prim")  
            print(get_func_time(algorithms_edgearr.prim, alg))

        elif line.strip() == "kruskal":
            print(algorithms_edgearr.kruskal_ALGraph.__doc__)
            ########### kruskal ###########
            edarr = EdgesetArray()
            edarr = edarr.load_csv(file_path = 'data/topo4.csv')
            # edarr = edarr.load_csv(file_path = 'data/GeneratedTopo_80points.csv')
            # tree = algorithms_edgearr.kruskal(edarr)
            # for x in tree:
            #     print(x[0]),
            #     print(x[1]),
            #     print(x[2])
            print("EdgesetArray for kruskal") 
            print(get_func_time(algorithms_edgearr.kruskal, edarr))     #more quick
            print("ALGraph for kruskal")  
            print(get_func_time(algorithms_edgearr.kruskal_ALGraph, alg))

        elif line.strip() == "topo":
            print(algorithms_edgearr.TopoSort.__doc__)
            ########### TopoSort ###########
            path, distance = director.CreatTourSortGraph(df1)
            print("start toposort, using DataFrame")
            print(get_func_time(algorithms_edgearr.TopoSort, path))
        else:
            print("wrong input, try again")
            continue

    

def get_func_time(func, *arg, **kw):
    """
    get the excute time for 2 functions, with same data
    maybe different datastructure
    """
    starttime = datetime.datetime.now() 
    func(*arg, **kw)    
    endtime = datetime.datetime.now()   
    return (endtime - starttime)
    

def start():
    """menu func
    """
    

    flag = False
    g = None
    path = None
    shortest_path = None
    file_path = None
    temp = utils.load_graph() #dataframe
    # temp = utils.load_graph(file_path = 'data/topo3.csv',
    # start_position = 1, end_position = 2, weight_positon = 3)
    while True:     
        print("welcome to tourism management system")
        print("plz enter a number:")
        print("1. input Scenic Spots graph or change graph")
        print("2. show Scenic Spots graph")
        print("3. show Tour guide Graph")
        print("4. show circle road in guide Graph")
        print("5. calculate shortest path and distance")
        print("6. show road constraction plan")
        print("7. search and sort Scenic Spots")
        print("8. parking system")
        print("9. algorithm compare")
        print("0. exit")  
        line = raw_input("enter sth, seperate by space, 0 for exit\n")
        

        if line.strip() == "1":
            file_path = raw_input("enter file name, 0 for a new csv file to store your graph\n")
            
            if file_path.strip() == "0":
                director.input_TourSortGraph()      #create csv file
                flag = True
                temp = utils.load_graph(file_path = 'data/graph1.csv',
            start_position = 0, end_position = 1, weight_positon = 2)
            else:
                
                temp = utils.load_graph(file_path = 'data/' + file_path.strip(),
            start_position = 1, end_position = 2, weight_positon = 3)

        elif line.strip() == "2":
            if flag:
                g = nxutil.load_csv_nx(file_path = 'data/graph1.csv')
            elif g == None:
                if file_path != None:
                    g = nxutil.load_csv_nx(file_path = 'data/' + file_path.strip())
                else:
                    g = nxutil.load_csv_nx()
            nxutil.show(g)
        elif line.strip() == "3":
            path, distance = director.CreatTourSortGraph(temp) 
            print("#"*40)
            for i in path:
                print(i)
            print("#"*40)   
            if g == None:
                if file_path != None:
                    g = nxutil.load_csv_nx(file_path = 'data/' + file_path.strip())
                else:
                    g = nxutil.load_csv_nx()
            nxutil.show(g)
        elif line.strip() == "4":
            if path == None:
                print("plz show Tour guide Graph first, now input 3")
                continue
            circle_path = algorithms_edgearr.TopoSort(path)
            if g == None:
                g = nxutil.load_csv_nx()
            nxutil.show(g, node_list = circle_path)

        elif line.strip() == "5":
            poi = raw_input("enter startpoint|endpoint, seperate by |, input -1 for a default value")
            if len(poi.strip().split("|")) != 1:
                # print chardet.detect(poi.strip().split("|")[0])
                start = unicode(poi.strip().split("|")[0], "GB2312")    # for windows console
                end = unicode(poi.strip().split("|")[1], "GB2312")
                
            else:
                print(len(poi.strip().split("|")))
                print(u"wrong format! use default instead: start from 北门, end in 碧水亭")
                start = u'北门'
                end = u'碧水亭'
            
            dist, shortest_path = algorithms.dijkstra(temp,  
                    start = start, 
                    end = end
                    )
            shortest_path.insert(0, start)
            shortest_path.append(end)
            for x in shortest_path:
                for y in x:
                    print(y)
                print("\n")
            if g == None:
                g = nxutil.load_csv_nx()
            nxutil.show(g, path_list = shortest_path)

        elif line.strip() == "6":
            dis_list, distance = algorithms.MST(temp)
            print(u"------------修路------------------")
            for x,y in dis_list:
                 print(x),
                 print(" --> "),
                 print(y)
            print(distance)
            if g == None:
                g = nxutil.load_csv_nx()
            nxutil.show(g, path_list = dis_list)

        elif line.strip() == "7":
            recommend.start(file_path)
            
        elif line.strip() == "8":
            parking.start()
        elif line.strip() == "9":
            compare()
        elif line.strip() == "0":
            break
        else:
            print("wrong input, try again")
            continue



if __name__ == '__main__':
    start()
    # main()
    # compare()
    # parking.start()
    # recommend.start()
    # g = nxutil.load_csv_nx(file_path = 'data/topo3.csv', start_position = 1, end_position = 2, weight_positon = 3)
    # g = nxutil.load_csv_nx()
    # nxutil.show(g)
