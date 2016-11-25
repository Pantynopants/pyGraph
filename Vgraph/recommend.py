# -*- coding=utf-8 -*-
import models
import utils
import random
import re
from operator import itemgetter, attrgetter 
from nx import utils as nxutil

def start(file_path):
    """
    reference
    ----------
    .. [1] http://blog.jobbole.com/21351/
    .. [2] http://www.jb51.net/article/64123.htm
    .. [3] http://www.jb51.net/article/87479.htm
    """
    user_input = None
    temp = models.EdgesetArray()

    utils.enhance_method(models.EdgesetArray, 'load_csv', add_comment)

    if file_path == None:
        file_path = "data/graph.csv"
    else:
        file_path = 'data/' + file_path.strip()
    temp = temp.load_csv(file_path = file_path)     # (score, comment)

    g = nxutil.load_csv_nx(file_path)

    while True:       
        print("welcome to tourism recommend system")
        print("plz enter a number:")
        print("1. sort Scenic Spots by their score")
        print("2. search Scenic Spots by name")
        
        print("0. exit")

        line = raw_input("enter sth, and 0 to exist")

        if line.strip() == "0":
            break
        
        elif line.strip() == "1":
            for k,v in sort_score(temp[0]):
                print(k),
                print(v)

        elif line.strip() == "2":
            start_point = raw_input("enter spots name you wanna visit")
            try:
                user_input = unicode(start_point.strip(), "GB2312")
            except:
                user_input = u'北门'
            
            if (type(temp[1].keys()[0]) != unicode):
                user_input = int(user_input)

            if user_input in temp[1].keys():
                print("Object find!")
                print(user_input),
                print(temp[1][user_input])
            else:
                print("View not find. Do you mean:")
                result_str_list = fuzzyfinder(user_input, temp[1])
                for i in result_str_list:
                    print(i)

            print(user_input, type(user_input))
            nxutil.show(g, node_list = [str(user_input).encode("utf-8").decode("utf-8")])
        else:continue
    

def add_comment(old_method, self, *args, **kwds):
    """
    for enhence methods

    """
    # print '*** calling: %s%s, kwds=%s' % (old_method.__name__, args, kwds)
    return_value = old_method(self, *args, **kwds)                  # call the original method
    v_number = return_value.get_all_vertexes()
    comment = {
        k:str(k).encode("utf-8").decode("utf-8")  + " is a good place"         # comment
        for k in v_number
    }
    score = {
        k: 5*random.uniform(0, 1) 
        for k in v_number
    }
    return (score, comment)                                 # as the return value of load_csv

def sort_score(score):
    """
    para
    -----
    score: dict

    return
    ------
    [(),]
    
    ref
    ---- 
    .. [1] http://gaopenghigh.iteye.com/blog/1483864
    """
    return sorted(score.iteritems(), key=itemgetter(1), reverse=True)   

def fuzzyfinder(user_input, comment):
    """
    para
    -----
    user_input:str
    comment: dict or list

    example
    --------
    >>> fuzzyfinder('user', collection)
    ['user_group.doc', 'api_user.doc']

    ref
    ----
    .. [1] http://blog.amjith.com/fuzzyfinder-in-10-lines-of-python
    """
    if type(comment) == dict:
        collection = comment.values() + comment.keys()
    elif type(comment) == list:
        collection = comment
    suggestions = []
    pattern = '.*?'.join(user_input)    # Converts 'djm' to 'd.*?j.*?m'
    regex = re.compile(pattern)        
    for item in collection:
        match = regex.search(item)      # Checks if the current item matches the regex.
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]