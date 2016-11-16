# -*- coding=utf-8 -*-
import Queue
from models import *

CAPACITY_ROAD = -1
CAPACITY_CARPARK = 5

def start():
    print("input simple:0 123123 2030")
    print("that means the car leave(0,enter by 1), number is 123123, time is 20:30")
    print("using space to split")
    carpark = []
    wait_field = []
    outside_road = Queue.Queue(maxsize = CAPACITY_ROAD)

    while True:       
        line = raw_input("enter sth, -1 to exist")
        if int(line.split()[0]) == -1:
            break
        data = line.split()
        if len(data) != 3:
            print("wrong input, plz try again")
            continue
        print(data)
