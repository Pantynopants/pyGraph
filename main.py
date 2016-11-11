# -*- coding=utf-8 -*-
from Vgraph import director
from models import *
import utils
def main():
    # director.CreatTourSortGraph(ALGraph())
    # temp = utils.load_csv_to_models()
    temp = utils.load_graph()
    path = director.DFSTraverse(temp) 
    for i in path:
        print(i)
    # for x in path:
    #     print(x)
    # print(list(path))
    # for x in list(path):
    #     print(x.decode('utf-8'))
if __name__ == '__main__':
    main()