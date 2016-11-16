# -*- coding=utf-8 -*-
from Vgraph import director, parking, recommend
from models import *
import utils
import algorithms
import algorithms_edgearr

# http://python.jobbole.com/81467/

def main():
    # director.CreatTourSortGraph(ALGraph())
    temp = utils.load_csv_to_models()
    print(temp)
    distance = 0
    # temp = utils.load_graph()
    # temp = temp[u"北门"]

    # for i in temp.index.index:
    #     print(i)
    # algorithms.floyd(temp)

    # path, distance = director.CreatTourSortGraph(temp) 
    # for i in path:
    #     print(i)
    # print("#"*40)    
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
    # temp.load_csv()
    # tree = algorithms_edgearr.kruskal(temp)
    # for x in tree:
    #     print(x[0]),
    #     print(x[1]),
    #     print(x[2])

    # for i,j in algorithms_edgearr.prim(temp):
    #     print(i), 
    #     print(j)

    for k,v in algorithms_edgearr.prim(temp).items():
        print(k), 
        print(v)

    print(distance)

def park():
    parking.start()

if __name__ == '__main__':
    # main()
    park()
