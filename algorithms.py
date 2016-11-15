# -*- coding=utf-8 -*-

import utils
import copy  
# tutorial http://stackoverflow.com/questions/22897209/dijkstras-algorithm-in-python
# http://www.cnblogs.com/biyeymyhjob/archive/2012/07/31/2615833.html
def dijkstra(graph, start = u'北门', end = None):
    """
    # TODO: change to ndarray
    para:
        DataFrame, str(unicode), str(unicode)
    return:distance from start to every point; the path from start point to others
        dist = {
        pointName:( distance = graph[start] (dataframe), isVisted = 0, path = [] )
        }
        or
        distance:number, path:list
    """    
    # dist:distance from start point to others
    # dist = {
    #   pointName:( distance = graph[start] (dataframe), isVisted = 0, path = [] )
    # }
    dis = zip(graph[start].index, graph[start])
    dist = {
        k:[v, 0, []]
        for k,v in dis            
    }
    for i in range(len(graph.index) - 1):
        mindis = utils.INF
        add_point = ""
        for k,v in dist.items():
            if v[1] == 0 and v[0] < mindis and v[0] > 0:
                mindis = v[0]
                add_point = k
        dist[add_point][1] = 1 # mark as visited
        for column_df_index in graph[add_point].index:
            
            if (graph.at[add_point, column_df_index] < utils.INF) and (dist[column_df_index][1] == 0):
                # print( (str(graph.at[add_point, column_df_index] + dist[add_point][0]) ) + "\t" + str(dist[column_df_index][0]))
                if dist[column_df_index][0] > graph.at[add_point, column_df_index] + dist[add_point][0]:
                    # print("update weight")
                    dist[column_df_index][0] =  graph.at[add_point, column_df_index] + dist[add_point][0]
                    
                    dist[column_df_index][2].extend(dist[add_point][2]) 
                    dist[column_df_index][2].append(add_point) 
                    # print(len(dist[column_df_index][2]))

    path = []
    for k,v in dist.items():
        temp_str = []
        temp_str.extend([x for x in v[2]])
        temp_str.extend([v[0], k])
        path.append(temp_str)    

    if end == None:        
        return dist, path
    else:
        return dist[end][0], dist[end][2]
    

def floyd(graph):
    """
    let all points' edges to simplified
    para:
        pd.dataframe
    return:
        pd.dataframe
    """
    result = graph.copy()
    points_list = result.index.tolist()
    point_dict = dict(zip([i for i in range(len(points_list))], points_list))
    
    result_matrix = result.as_matrix()
    # Floyd-Warshall algorithm
    for k in range(len(result_matrix)):
        for i in range(len(result_matrix)):
            for j in range(len(result_matrix)):
                if(result_matrix[i][k] < utils.INF and result_matrix[k][j] < utils.INF and result_matrix[i][j] > result_matrix[i][k] + result_matrix[k][j]):
                    
                    result.set_value(point_dict[i], point_dict[j], result_matrix[i][k] + result_matrix[k][j])
                    result.set_value(point_dict[j], point_dict[i], result_matrix[i][k] + result_matrix[k][j])

                    result_matrix[i][j] = result_matrix[i][k] + result_matrix[k][j] 
    return result