#Possible future work:
###Extend to define entrances as exits 
###Add gpu functionality
###Add buffer for manual selection

from utils.map import map 
from utils.wanderer import wanderer as wand

#####

import numpy as np 
import matplotlib.pyplot as plt
import sys, os, binascii
from collections import deque
from random import choice
from random import randrange as rr

from numpy import array as arr

from PIL import Image as im
from timeit import default_timer as timer

#I couldn't figure out how to work with the keypresses so I set this up against my better judgement

def generation_info(runs, tunnel_vision, min_wander, min_density,max_density,dirpath):
    path = os.path.join(dirpath,"config_file.txt")
    with open(path, 'w') as cf:
        cf.write(f"runs: {runs} \ntunnel_vision: {tunnel_vision}\nminimum wander: {min_wander}\nmin_density: {min_density}\nmax_density: {max_density}")
        cf.close()

def progress_bar(progress, total,**running_sum ):
    percent = 100 * (progress / float(total))
    bar = '▄' * int(percent) + '-' * (100-int(percent))
    print(f"\r {running_sum['running_sum']} |{bar} | {percent:.2f}%", end="\r")

def autobot(runs, tunnel_vision, min_wander, min_density,max_density, folder): #autodownload procgen imgs
    sum = 0
    start  = timer()
    dirpath = str(binascii.b2a_hex(os.urandom(8)).decode('latin-1'))
    dirpath = os.path.join(folder,dirpath)
    largest = 0
    os.mkdir(dirpath)
    generation_info(runs, tunnel_vision, min_wander, min_density,max_density,dirpath)
    for i in range(runs):
        mapper = wand(min_wander) # wanderer( arr([starting position]) ,  min_wander_distance_before_can_leave_box )
        path_data = mapper.get_path_data(tunnel_vision) #get the paths taken by wanderer
        map_profile = map(path_data) #get text map 10 x 10
        if not map_profile.is_two_way:
            map_profile.generate()
            graph = map_profile.console_map
            w_measure = 0 
            size = float(graph.size)
            graph = graph.flatten()
            w_measure = np.count_nonzero(graph == 'w')
            largest = w_measure if largest < w_measure else largest
            
            density = w_measure/size 
            if density >= min_density and density <= max_density:
                    map_profile.save(dirpath)
                    sum += 1
            progress_bar(i, runs-1,running_sum=largest)

    print("largest w_measure: " + str(largest) + " found: "+str(sum) + " at: "+ str(timer()- start) + "    ")


def main():
    fig,ax  = plt.subplots()
    cid = fig.canvas.mpl_connect('key_press_event',manual)
    folder = "E:\RandomWalkPictures"
    autobot(10_000,50,25,0.40,0.55,folder)
    #I'll figure this out later
    pass
   
if __name__=="__main__":
    main()













