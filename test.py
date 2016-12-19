# -*- coding=utf-8 -*-
from using_alg import TSP
from models import *
import utils

import sys
import os
# import chardet
import datetime

reload(sys)
sys.setdefaultencoding( "utf-8" )

def main():
    # temp = utils.load_graph()
    # TSP.TSP(graph = temp, start = u'北门')

    TSP.test()

if __name__ == '__main__':
    main()