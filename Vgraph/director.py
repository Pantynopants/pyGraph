# -*- coding=utf-8 -*-
from models import *
import algorithms
import utils
import pandas as pd
import copy 
import os
ls = os.linesep

def input_TourSortGraph():
    """
    create csv file by user input
    """
    csv_poi = []
    csv_poi.append("start,end,weight")
    while True:       
        line = raw_input("enter sth, separate by ',' and -1 to exist")

        
        if line.strip() == "-1":
            break
        data = line.split(',')
        if len(data) != 3:
            print("wrong input, plz try again")
            continue
        
        csv_poi.append(line.strip())


    fobj = open("data/graph1.csv",'w') 
    fobj.writelines(['%s%s' % (x,ls) for x in csv_poi ])
    fobj.close()
    print 'DONE!'

@utils.get_total_dist
def CreatTourSortGraph(graph):
    """
    para:
        ALGraph or dataframe
    return: tour route
        list
    """
    if utils.graph_type(graph)[0] == "ALGraph":
        return
    else:
        (dfs_visit, path), dist = algorithms.DFSTraverse(graph, start = graph.columns.values[0])
        i = 0
        while i < len(dfs_visit) - 1:
            # if is_fin(dfs_visit[:i+2], graph.index):
            #     return dfs_visit[:i+2]
            if dfs_visit[i+1] not in utils.LocateVex(graph, dfs_visit[i]):
                _, templist = algorithms.dijkstra(graph, start = dfs_visit[i], end = dfs_visit[i+1])
                for insert_poi in templist:                    
                    dfs_visit.insert(i+1, insert_poi)    
                    i += 1     
                
            else:               
                i += 1

        return dfs_visit
        

########### helper func ###########
def getInDegree(DGlist):
    """
    using indegree_list = edarray.get_indegrees() instead
    para:
        list
    return:
        degree_dict = {pointname:point_indegree}
    """
    pass


def IsEdge():
    pass


def is_fin(current_list, view_list):
    """
    check whether the rote of director is finished
    para: viewlist means points you'v visited
        list
    return:
        T if finished
        F if not
    """
    print("*"*100)
    if len(current_list) < len(view_list):
        return False
    for x in view_list:
        if x not in current_list:
            return False
    return True

