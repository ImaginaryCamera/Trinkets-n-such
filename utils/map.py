import cv2
import numpy as np
import os, binascii
import matplotlib.pyplot as plt
from numpy import array as arr
import array
from PIL import Image as im


class map(): 
    def __init__(self, path_data):
        self.line = arr(['.','.','.','.','.','.','.','.','.','.',])
        self.console_map = self.lazy_make_map()
        self.graph = 255* np.ones(shape=[500,500,3], dtype=np.uint8)
        self.filename = ''
        self.image = 0
        self.path_data = path_data
        self.entrance = path_data[0]
        self.exit = path_data[-1]
        self.is_two_way = self.check_two_way()
    
    def lazy_make_map(self):
        _map = []
        for _ in range(10):
           _map.append(self.line)
        _map = np.asarray(_map)
        return _map

    def generate(self):
        a = [self.entrance, self.exit]
        for item in self.path_data: #replace position with x to mark navigable map
            
            if np.array_equal(item,self.entrance):
                self.console_map[item[1]][item[0]] = 'e'
                cv2.rectangle(self.graph, pt1=(item[0] * 50, item[1] * 50), pt2=((item[0] + 1) * 50, (item[1] + 1) * 50), color=(0,255,0), thickness = -1)
            elif  np.array_equal(item,self.exit):
                self.console_map[item[1]][item[0]] = 'x'
                cv2.rectangle(self.graph, pt1=(item[0] * 50, item[1] * 50), pt2=((item[0] + 1) * 50, (item[1] + 1) * 50), color=(255,0,0), thickness = -1)
            else:
                self.console_map[item[1]][item[0]] = 'w'
                cv2.rectangle(self.graph, pt1=(item[0] * 50, item[1] * 50), pt2=((item[0] + 1) * 50, (item[1] + 1) * 50), color=(0,0,0), thickness = -1)

            
        self.image = im.fromarray(self.graph)
        self.filename = str(binascii.b2a_hex(os.urandom(8)).decode('latin-1'))

    def save(self, directory):
        if (directory == '') and self.image != 0:
            fullpath = os.path.abspath(".\\"+self.filename+".png")
            self.image.save(fullpath)
        elif (directory != '') and self.image != 0:
            fullpath = os.path.join(directory, self.filename + ".png")
            self.image.save(fullpath)

    def show(self):
        plt.imshow(self.map_profile.graph)
        plt.show()
        print(self.map_profile.console_map)

    def check_two_way(self):
        a = array.array('i',[0,9])
        if self.entrance[0] == self.exit[0] and self.entrance[0] in a:
            return True
        elif self.entrance[1] == self.exit[1] and self.entrance[1] in a:
            return True
        else:
            return False


    