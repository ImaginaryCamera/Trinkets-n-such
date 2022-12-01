#Possible future work:
###Add gpu functionality
###Add buffer for manual selection


import numpy as np 
import matplotlib.pyplot as plt
import cv2
import sys
import os, binascii
from random import choice
from random import randrange as rr
from random import random as rand
from numpy import array as arr
from math import sin, cos, pi
from PIL import Image as im
from timeit import default_timer as timer

#I couldn't figure out how to work with the keypresses so I set this up against my better judgement
PAJDHFCVRE = 0
FAODSKLNVR = '' 

class vagabond(): #the basic random walker
    def __init__(self, location, min_travel_dist):
        self.direction = arr([1,0])
        self.min_travel_dist = min_travel_dist
        self.dist_travelled = 0
        self.location = location
        self.journey_complete = False
           
    def drive(self):
        next_move = self.direction + self.location
        if self.validate(next_move) == 1:
            self.location = next_move
            self.dist_travelled += 1
            return self.location
            
        elif self.validate(next_move) == -1:
            self.steer()
            return self.location

        else:
            return None
            
    def validate(self, next_move):
        y_out_of_bound = True if next_move[1] <= -1 or next_move[1] >= 10 else False
        x_out_of_bound = True if next_move[0] <= -1 or next_move[0] >= 10 else False

        out_of_bounds = y_out_of_bound or x_out_of_bound
        is_free = False if (self.dist_travelled <= self.min_travel_dist) else True
        if out_of_bounds and not is_free:
            return -1
        elif not out_of_bounds and not is_free:
            return 1
        elif out_of_bounds and is_free:
            self.journey_complete  = True
            return None
        else:
            return 1
            
    def steer(self):
        steer_left = choice([True,False])
        _x = self.direction[0]
        _y = self.direction[1]
        if steer_left:
            self.direction[0] = _x * cos(pi/2) - _y * sin(pi/2)
            self.direction[1] = _x * sin(pi/2) + _y * cos(pi/2)
        else:
            self.direction[0] = _x * cos(-pi/2) - _y * sin(-pi/2)
            self.direction[1] = _x * sin(-pi/2) + _y * cos(-pi/2)
      
    def get_path_data(self, drive_tendency):
        path_data = []
        path_data.append(np.copy(self.location))
        if drive_tendency <=100:
            while self.journey_complete == False:
                if rand() >= drive_tendency/100:
                    path_data.append(np.copy(self.drive()))
                else:
                    self.steer()
            return path_data
        else:
            print("please enter a percetage% value")

class map(): #a text based map if you want one
    def __init__(self, path_data):
        self.line = arr(['.','.','.','.','.','.','.','.','.','.',])
        self.lazy_make_map()
        self.console_map
        self.graph = 255* np.ones(shape=[1000,1000,3], dtype=np.uint8)
        self.path_data = path_data
    
    def lazy_make_map(self):
        self.console_map = arr([self.line])
        for _ in range(9):
            self.console_map = np.append(self.console_map, [self.line], axis=0)
    def generate(self):
        
        for item in self.path_data: #replace position with x to mark navigable map
            if item.any() != np.array(None):
                cv2.rectangle(self.graph, pt1=(item[0] * 100, item[1] * 100), pt2=((item[0] + 1) * 100, (item[1] + 1) * 100), color=(0,0,0), thickness = -1)
                self.console_map[item[1]][item[0]] = 'x'
        
def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '▄' * int(percent) + '-' * (100-int(percent))
    print(f"\r|{bar} | {percent:.2f}%", end="\r")

def get_edge():
    return choice(
        [
            arr([0,rr(0,10)]),
            arr([9,rr(0,10)]),
            arr([rr(0,10),0]),
            arr([rr(0,10),9]),
        ]
    )

def rollout(): #autodownload procgen imgs
    sum = 0
    runs = 1000  
    start  = timer()
    for i in range(runs):
        mapper = vagabond(get_edge() , 35) # vagabond( arr([starting position]) ,  min_wander_distance_before_can_leave_box )
        path_data = mapper.get_path_data(35) #get the paths taken by vagabond
        map_profile = map(path_data) #get text map 10 x 10
        map_profile.generate()
        graph = map_profile.console_map
        x_measure = 0 
        size = float(graph.size)
        graph = graph.flatten()
        x_measure = np.count_nonzero(graph == 'x')
        density = x_measure/size 
        if density >= 0.50 and density <= 0.70:
            image = im.fromarray(map_profile.graph)
            filename =  str(binascii.b2a_hex(os.urandom(8)).decode('latin-1'))
            fullpath = os.path.join("E:\RandomWalkPictures", filename + '.' + "png")
            image.save(fullpath)
            sum += 1
        progress_bar(i, runs)

    print("found: "+str(sum) + " at: "+ str(timer()- start))

def manual(event):
    global PAJDHFCVRE  #picture
    global FAODSKLNVR  #filename
    print('press', event.key)
    sys.stdout.flush()
    filename = ''
    img = 0
    if event.key == "right":
        mapper = vagabond(arr([9,0]) , 15) # vagabond( arr([starting position]) ,  min_wander_distance_before_can_leave_box )
        path_data = mapper.get_path_data(99) #get the paths taken by vagabond
        map_profile = map(path_data) #get text map 10 x 10
        map_profile.generate()
        filename =  str(binascii.b2a_hex(os.urandom(8)).decode('latin-1'))
        image = im.fromarray(map_profile.graph)
        PAJDHFCVRE = image
        FAODSKLNVR = filename
        print(PAJDHFCVRE)
        plt.imshow(map_profile.graph)
        plt.show()
        print(map_profile.console_map) # print to console

    elif event.key == "down":
        print(type(PAJDHFCVRE))
        fullpath = os.path.join("C:\\Users\\Cache\\Pictures\\RandomPic", FAODSKLNVR + '.' + "png")
        PAJDHFCVRE.save(fullpath)
        print("saved")


def main():
    fig,ax  = plt.subplots()
    cid = fig.canvas.mpl_connect('key_press_event',manual)
    #I'll figure this out later
    pass
   
if __name__=="__main__":
    main() # does nothing atm













