# -*- coding=utf-8 -*-
from Vgraph import director

# tutor http://stackoverflow.com/questions/22897209/dijkstras-algorithm-in-python
def dijkstra(graph, start, end):
    """
    para:
        DataFrame, str, str
    return:
        path:list
    """
    graph_matrix = graph.as_matrix()
    visited = []
    dist = {}
    for i in range(len(graph.index)):
        # dist
        visited.append(False)

def floyd(result):
    """
    let all points' edges to simplified
    para:
        pd.dataframe
    return:
        pd.dataframe, martix(list(list))
    """
    points_list = result.index.tolist()
    point_dict = dict(zip([i for i in range(len(points_list))], points_list))
    
    result_matrix = result.as_matrix()
    # Floyd-Warshall algorithm
    for k in range(len(result_matrix)):
        for i in range(len(result_matrix)):
            for j in range(len(result_matrix)):
                if(result_matrix[i][k] < INF and result_matrix[k][j] < INF and result_matrix[i][j] > result_matrix[i][k] + result_matrix[k][j]):
                    
                    result.set_value(point_dict[i], point_dict[j], result_matrix[i][k] + result_matrix[k][j])
                    result.set_value(point_dict[j], point_dict[i], result_matrix[i][k] + result_matrix[k][j])

                    result_matrix[i][j] = result_matrix[i][k] + result_matrix[k][j] 
    return result, result_matrix