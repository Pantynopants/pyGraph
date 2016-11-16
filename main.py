# -*- coding=utf-8 -*-
from Vgraph import director
from models import *
import utils
import algorithms
import algorithms_edgearr
def main():
    # director.CreatTourSortGraph(ALGraph())
    # temp = utils.load_csv_to_models()
    distance = 0
    temp = utils.load_graph()
    # temp = temp[u"北门"]

    # for i in temp.index.index:
    #     print(i)
    # algorithms.floyd(temp)

    path, distance = director.CreatTourSortGraph(temp) 
    # for i in path:
    #     print(i)
    # print("#"*40)
    algorithms_edgearr.TopoSort(path)


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
    print(distance)

if __name__ == '__main__':
    main()
