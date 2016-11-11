# -*- coding=utf-8 -*-
from collections import Mapping
# from collections.abc import Mapping

class ALGraph(Mapping):
    """docstring for ALGraph"""
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
    


"""
graph = {'A': {'B':1, 'C':2},
         'B': {'A':1, 'D':2, 'E':3},
         ...}
optimize
http://www.kr41.net/2016/03-23-dont_inherit_python_builtin_dict_type.html
http://stackoverflow.com/questions/3387691/python-how-to-perfectly-override-a-dict
http://stackoverflow.com/questions/2390827/how-to-properly-subclass-dict-and-override-getitem-setitem
"""    