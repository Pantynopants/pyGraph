# -*- coding=utf-8 -*-
from collections import Mapping
import numpy as np
import pandas as pd
# from collections.abc import Mapping

class ALGraph(Mapping):
    """ALGraph
    same operation as dict

    using:
    >>> graph = {'A': {'B':1, 'C':2},
         'B': {'A':1, 'D':2, 'E':3},
         ...}

    """
    def __init__(self, *args, **kwargs):
        self._storage = dict(*args, **kwargs)
    def __setitem__(self, key = "", val = {}):  
        
        self._storage[key] = val
    def __getitem__(self, key = ""):  
        # val = dict.__getitem__(self, key)
        
        return self._storage[key]
    def update(self, *args, **kwargs):
        # print 'update', args, kwargs
        for k, v in dict(*args, **kwargs).iteritems():
            self._storage[k] = v
    def __iter__(self):
        return iter(self._storage)  
    def __len__(self):
        return len(self._storage)
    def pop(self, key):
        if type(key) == list or type(key) == set:
            for i in key:
                if i not in self._storage.keys():
                    continue
                del(self._storage[i])
            return self._storage.keys()
        result = self._storage[key]
        del(self._storage[key])
        return result
    def __repr__(self):
        dictrepr = dict.__repr__(self._storage)
        # return '%s(%s)' % (type(self).__name__, dictrepr)
        return '%s' % (dictrepr)

class VNode(object):
    """point of view"""
    def __init__(self, name = "", nextArcNode = {}):        
        super(VNode, self).__init__()
        self.name = name
        self.nextArcNode = nextArcNode        

        
class ArcNode(ALGraph):
    """road """
    def __init__(self, *args, **kwargs):
        self._storage = dict(*args, **kwargs)
    
class EdgesetArray(object):
    """ EdgesetArray
    compaired with .csv file,  it added the list of vertex
    also indegree recoding
    
    property:
        vertex(_v): pd.dataframe 
        edge(_e): pd.dataframe
        
    """
    
    def __init__(self, v = [], e = None):
        """
        v: unicode list
            list of vertex
        e: 2D list
            every edges
        """
        super(EdgesetArray, self).__init__()
        self.df_index = [u"start", u"end", u"weight"]

        self._v = pd.DataFrame(np.zeros( (1, len(v) ) ), columns = v, index = ["0"]) 


        self._e = pd.DataFrame(columns = self.df_index)
        if type(e) != pd.DataFrame and e != None:
            # e = [ [x,x,x],
            #   [x,x,x],
            # ...
            # ]
            self._e = pd.DataFrame(np.array(e), columns = self.df_index)
        
 
    def get_edge(self, start_poi, end_poi):
        """
        check if "start" column and "end" column can meet the parameter
        para:
            unicode, unicode
        return:
            pd.dataframe
        """
        # del_poi_as_start = self._e[ self._e[u"start"] == name]
        start_list = self._e[ self._e[u"start"] == start_poi]
        end_list = self._e[ self._e[u"end"] == end_poi]
        indexs = [i for i in start_list.index if i in end_list.index]
        return indexs
    
    def set_edge(self, index, val):
        """
        para:
            index of the edge
        """
        self._e[index] = val
        return self

    def add_edge(self, start, end, weight):
        """
        add 1 row each time
        then update the indegree list
        para:
            unicode, unicode, int
        """
        if len(self.get_edge(start, end)) != 0: # this edge already exist
            return
        s1 = pd.DataFrame({u"start":start, u"end":end, u"weight":weight}, index=[len(self._e)])
        # self._e.append(s1, ignore_index=True )
        self.update_indegree(end)
        self._e = pd.concat([self._e, s1], axis = 0)
        # self._e.reindex(range(len(self._e)))
        # print(self._e)

    def del_edge(self, start = None, end = None):
        """
        better to use keyword delete 1 edge
        """
        # print(end)
        self.update_indegree(end, -1) 
        # print(len(self._e))
        print(self.get_edge(start, end))
        self._e = self._e.drop(self.get_edge(start, end))
        # print(len(self._e))
                       

    edge = property(get_edge, set_edge, del_edge)

    def get_vertex(self, vertexid):
        """
        according to
        http://blog.chinaunix.net/xmlrpc.php?r=blog/article&uid=23100982&id=3540311
        index canbe anytype, both int and unicode -> vertexid
        """
        # if type(vertexid) == unicode and type(vertexid) == int :
        #    return self._v[vertexid] # degree of the point
        # print(vertexid)
        return self._v[vertexid]
    
    def set_vertex(self, vertexid, val):
        self._v[vertexid] = val

    def del_vertex(self, name = ""):
        """
        para: name of vertex
            unicode
        """
        
        # self.del_edge(point_name = name)
        # print(self._e.loc[:, [u"start"]])
        del_poi_as_start = self._e[ self._e[u"start"] == name]
        # print(del_poi_as_start.index)
        # print(del_poi_as_start.loc[:, [u"end"]])

        # target_index = [0]
        # while len(target_index) != 0:
        #     target_index = self._e[ self._e[u"start"] == name].index
        #     i = target_index[0]
        indexs = [i for i in del_poi_as_start.index]
        # print(indexs)
            # print(self._e.iloc[i, :][u"end"])
            # print(self._e.iloc[i,[u"end"] ])
        # print(type(name), type(self._e.iloc[indexs, :][u"end"]), type(self._e.loc[0, u"end"]))
        # print(name), 
        # print(self._e.loc[15, u"start"])

        # self.del_edge(name, self._e.loc[0, u"end"])
        while indexs:  
            # print("success")       
            self.del_edge(name, self._e.loc[indexs[0], u"end"])
            del_poi_as_start = self._e[ self._e[u"start"] == name]
            indexs = [i for i in del_poi_as_start.index]
        
        # del_poi_as_end = self._e[ self._e.loc[:, [u"end"]].isin([name])]
        del_poi_as_end = self._e[ self._e[u"end"] == name]
        indexs = [i for i in del_poi_as_end.index]
        # print(del_poi_as_end)
        # print(self._e)
        while indexs:  
            # print("success")  
            # print(indexs) 
            # print(self._e.loc[indexs[0], u"start"]),
            # print(name)    
            self.del_edge(self._e.loc[indexs[0], u"start"], name)
            del_poi_as_end = self._e[ self._e[u"end"] == name]
            indexs = [i for i in del_poi_as_end.index]
        

        # self._e = self._e.drop( self._e[ self._e.loc[u"start"].isin(point_name)].index )
        # self._e = self._e.drop( self._e[ self._e.loc[u"end"].isin(point_name)].index )
        self._v = self._v.drop(name, 1) # axis=1 to drop a column, 0 to row
        
        return self

    vertex = property(get_vertex, set_vertex, del_vertex)
    

    def route_to_edgeSetArray(self, route_list):
        """
        change self, from a point chain to a edges set
        para:
            route_list: (unicode) list
        return:
            Edgesetarray
        """
        for i in range(len(route_list) - 1):
            self.add_edge(route_list[i], route_list[i+1], 1) # ignore weight here, set 1
        print(self._e)
        return self

    def update_indegree(self, end_poi, operation = 1):
        """helper func
        for every time add a edge, +1 indegree
        del an edge, -1
        """
        # print(end_poi),
        # print(operation)
        self.set_vertex(end_poi, self.get_vertex(end_poi) + operation)

    def get_indegrees(self):
        """
        return:
            dict{name:indegree}
        """
        return self._v

    def get_all_edges(self):
        return self._e
    

    # some operation of series see:www.cnblogs.com/smallcrystal/p/5809864.html

"""

optimize
http://www.kr41.net/2016/03-23-dont_inherit_python_builtin_dict_type.html
http://stackoverflow.com/questions/3387691/python-how-to-perfectly-override-a-dict
http://stackoverflow.com/questions/2390827/how-to-properly-subclass-dict-and-override-getitem-setitem
"""    