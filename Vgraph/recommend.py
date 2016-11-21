# -*- coding=utf-8 -*-
import models
import utils
import random
import re
from operator import itemgetter, attrgetter 

def start():
    """
    reference
    ----------
    .. [1] http://blog.jobbole.com/21351/
    .. [2] http://www.jb51.net/article/64123.htm
    .. [3] http://www.jb51.net/article/87479.htm
    """


    temp = models.EdgesetArray()
    utils.enhance_method(models.EdgesetArray, 'load_csv', add_comment)

    temp = temp.load_csv()
    # print temp[1]
    # print sort_score(temp[0])
    user_input = u'北门'
    if user_input in temp[1].keys():
        print("Object find!")
        print(user_input),
        print(temp[1][user_input])
    else:
        print("View not find. Do you mean:")
        result_str_list = fuzzyfinder(user_input, temp[1])
        for i in result_str_list:
            print(i)

def add_comment(old_method, self, *args, **kwds):
    """
    for enhence methods

    """
    # print '*** calling: %s%s, kwds=%s' % (old_method.__name__, args, kwds)
    return_value = old_method(self, *args, **kwds) # call the original method
    v_number = return_value.get_all_vertexes()
    comment = {
        k:k*5
        for k in v_number
    }
    score = {
        k: 5*random.uniform(0, 1) 
        for k in v_number
    }
    return (score, comment)

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