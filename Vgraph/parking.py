# -*- coding=utf-8 -*-
import Queue
from models import *

CAPACITY_ROAD = -1
CAPACITY_CARPARK = 3
carpark = [] #[(car_number, time)]
wait_field = [] #[(car_number, time)]
outside_road = Queue.Queue(maxsize = CAPACITY_ROAD) #[(car_number, time)]

def start():
    print("WEICOME TO PARKING SYSTEM!")
    print("input simple:0 123123 2030")
    print("that means the car leave(0, enter by 1), number is 123123, time is 20:30")
    print("using space to split")
    while True:       
        line = raw_input("enter sth, separate by space ' ', -1 to exist")
        if line.strip() == "-1":
            break
        print("carpark and waitfield")
        print(carpark)
        print(wait_field)
        for i in list(outside_road.queue): print(i)
        try:
            data = line.split()
        except :
            print("wrong input! plz try again")
            continue
        
        if len(data) != 3:
            print("wrong input, plz try again")
            update()
            continue
             
        # print(data)
        if int(data[0]) == 0:
            print("withdraw")
            withdraw(data[1], data[2])
        elif int(data[0]) == 1:
            checkin(data[1], data[2])
        else:print("wrong command, plz try again")
        

def checkin(car_number, time):
    """let the car in stack or wait, in that time
    Parameters
    -----
    car_number:int/str
    time:str
    Returns
    ------
    position:int 
        position of new car
    """
    if not is_carpark_avaliable(): # put it in outside_road        
        outside_road.put((car_number, time))
        position = outside_road.qsize() + CAPACITY_CARPARK  
    else:
        if not is_outside_road_empty():carpark.append(outside_road.get())  
        else: carpark.append((car_number, time))  
        position = len(carpark)   
    update()

    return position

def withdraw(car_number, time):
    """
    Parameters
    -----
    car_number:int/str
    time:str
    Returns
    -------
    car_index:int
    delta_time:int
    """
    in_carpark = filter(lambda x: x[0] == car_number, carpark)
    in_waitfield = filter(lambda x: x[0] == car_number, wait_field)
    print(in_carpark)
    print(in_waitfield)
    if len(in_carpark) != 0: # withdraw from carpark        
        car_index = carpark.index(in_carpark[0])
        delta_time = int(time) - int(carpark[car_index][1])
        print("car position: " + str(car_index))
        print("car parking time: " + str(delta_time))
        if car_index<len(carpark): wait_field.extend(carpark[car_index+1:])
        del carpark[car_index]
        
    elif len(in_waitfield) != 0: # withdraw from waitfield
        # TODO        
        car_index = wait_field.index(in_waitfield[0])
    else:
        print("car not in")
        return
    update()
    return car_index, delta_time

def update():
    """helper function for store in stack or queue
    """
    while not is_outside_road_empty and is_carpark_avaliable: gointo_carpark()
    while not is_waitfield_empty and is_carpark_avaliable: fulfill()

gointo_carpark = lambda : carpark.append(outside_road.get())

fulfill = lambda : carpark.append(wait_field.pop())

is_carpark_avaliable = lambda : len(carpark) <= CAPACITY_CARPARK

is_waitfield_empty = lambda : len(wait_field) == 0

is_outside_road_empty = lambda : outside_road.qsize() == 0
