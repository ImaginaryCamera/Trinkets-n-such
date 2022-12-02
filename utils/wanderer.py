import numpy as np
from numpy import array as arr
from collections import deque
from random import choice
from random import randrange as rr
from math import sin, cos, pi
from random import random as rand

class wanderer(): #the basic random walker
    def __init__(self, min_travel_dist):
        self.direction = arr([1,0])
        self.min_travel_dist = min_travel_dist
        self.dist_travelled = 0
        self.location = self.get_edge() #non-corners
        self.journey_complete = False
           
    def drive(self):
        next_move = self.direction + self.location
        if self.validate(next_move) == 1:
            self.location = next_move
            self.dist_travelled += 1
            return self.location
            
        elif self.validate(next_move) == 0:
            self.steer()
            return self.location

        else:
            return self.location
            
    def validate(self, next_move):
        y_out_of_bound = True if next_move[1] <= 0 or next_move[1] >= 9 else False
        x_out_of_bound = True if next_move[0] <= 0 or next_move[0] >= 9 else False

        out_of_bounds = y_out_of_bound or x_out_of_bound
        is_free = False if (self.dist_travelled <= self.min_travel_dist) else True
        if out_of_bounds and not is_free:
            return 0
        elif not out_of_bounds and not is_free:
            return 1
        elif out_of_bounds and is_free:
            self.journey_complete  = True
            return 1
        else:
            return 1
            
    def steer(self):
        steer_left = choice([True,False])
        _x = self.direction[0]
        _y = self.direction[1]
        if steer_left:
            self.direction[0] = _x * int(cos(pi/2)) - _y * int(sin(pi/2))
            self.direction[1] = _x * int(sin(pi/2)) + _y * int(cos(pi/2))
        else:
            self.direction[0] = _x * int(cos(-pi/2)) - _y * int(sin(-pi/2))
            self.direction[1] = _x * int(sin(-pi/2)) + _y * int(cos(-pi/2))

    def get_path_data(self, drive_tendency):
        path_data = deque()
        path_data.append(self.location)
        if drive_tendency <=100:
            while self.journey_complete == False:
                if rand() >= drive_tendency/100:
                    path_data.append(self.drive())
                else:
                    self.steer()
            return path_data
        else:
            print("please enter a percetage% value")
    
    def get_edge(self):
        _max = [0,9]
        return choice(
        [
            arr([choice(_max),rr(1,8)]),
            arr([rr(1,8),choice(_max)]),

        ]
    )