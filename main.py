# -*- coding=utf-8 -*-
from Vgraph import director
from models import *
import utils
import algorithms
def main():
    # director.CreatTourSortGraph(ALGraph())
    # temp = utils.load_csv_to_models()

    temp = utils.load_graph()
    # algorithms.floyd(temp)
    path = director.CreatTourSortGraph(temp) 
    for i in path:
        print(i)
    print("#"*40)
    director.TopoSort(path, temp)
    # path = director.DFSTraverse(temp) 
    # for i in path:
    #     print(i)
    # print("#"*40)
    # _, path = algorithms.dijkstra(temp)
    # for x in path:
    #     for y in x:
    #         print(y)
    #     print("\n")

if __name__ == '__main__':
    main()
