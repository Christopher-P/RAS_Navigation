#!/usr/bin/env python


'''
The goal behind this code is the following:
To subscribe to the ROS Topic for 'global/costmap'
From that we will pull the raw information with a 2D array of points. 
For the moment my small test set will have points from 0 to 2.
After we get the data, we will need to figure out where RAS is inside that
costmaps points. 

When this service is called it will also need the proposed point RAS should move to. 
We will check where that point is, if it is inside a collision/inflation point we 
want to pick the next closest point.

In this current version you don't need to know RAS' position. What you're looking for
in this case is the closest free space from an point that isn't allowed to be moved in.
'''


import rospy, math, time, sys, os, random
import numpy as np
# from tf import TransformListener
# from ras_msgs.srv import Localize


#Setup the map to use, I'll need to mess with this once I get actual costmap so
#I can make sure numpy has it oriented properly, or preferably we can work with it directly
#As given. Will still need to ensure the x,y is properly oriented with what I have here. 
class NewMap():


    #When we get costmap we will pass it here and just have it be the map, hopefully. 
    def __init__(self):

        with open("fakemap.txt") as textFile:
            lines = [line.split() for line in textFile]

        self.Map = np.array(lines, dtype=np.int8)
        self.Map = np.flipud(self.Map)
        #This is to make the coordinates traditional bottom,left is 0,0
        #However this needs to be double checked with an actual costmap to see what the orientation is.


    #Delete soon, was function used to make fake maps
    def changeIt(self, start, end, row, changeTo):

        for i in range (start, end + 1):
            self.Map[row][i] = changeTo


    #Remove when visuals not needed
    def printMap(self):

        np.set_printoptions(threshold='nan')
        print(self.Map)


    #Returns T/F for if the requested point is acceptable or not.
    def wantedPoint(self, point):
        if self.Map[point[0]][point[1]] > 30: return False
        else: return True


    #Finds the closest free point to your requested point, using spiral pattern.
    def closestPoint(self, point):
        #https://stackoverflow.com/questions/398299/looping-in-a-spiral
        #Going to search for points in a spiral out from original point. 
 
        shape = self.Map.shape
        print(shape) #Debug
        row_count = shape[0]
        col_count = shape[1]
        row = col = 0
        d_row = 0
        d_col = -1

        for i in range(max(row_count, col_count)**2):

            if row == col or (row < 0 and row == -col) or (row > 0 and row == 1 - col):
                d_row, d_col = -d_col, d_row

            row, col = row + d_row, col + d_col

            new_row = point[0] + row 
            new_col = point[1] + col
            in_bounds = (0 <= new_row < row_count) and (0 <= new_col < col_count)
            
            if in_bounds and self.wantedPoint((new_row, new_col)):
                self.Map[new_row, new_col] = 11 #to see ending point, remove when visuals not needed
                return (new_row, new_col)
            elif in_bounds:
                self.Map[new_row][new_col] = 33 #To see path, remove when visuals not needed
            

if __name__ == '__main__':
   
    try:

        map = NewMap()            
        point = (12, 00) #row, col not x,y with numpy
        acceptable = map.wantedPoint(point)
        map.Map[point] = 77 #To see start

        while not acceptable: 
            point = map.closestPoint(point)
            acceptable = map.wantedPoint(point)

        map.printMap() #Delete later, debug reasons now. 


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(e)

    # except rospy.ROSInterruptException:
    #     rospy.loginfo("Exception thrown")
