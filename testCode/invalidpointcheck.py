#!/usr/bin/env python


'''
This service will take a point given to use in the local map. 
The map of the room will be processed into numpy grid. 
Given the point we will find it in the numpy grid. 
We will decide if it is an acceptable point below the threshold. 
Once we find that point we will return it in right coordinates. 
The coordiates we return are in the same format as the given ones.
'''


import rospy, random
import numpy as np

 
class NewMap():


    #Given the text file of the map we find all the needed data.
    def __init__(self, m_file, th):

        self.th, self.m_file = th, m_file
        self.Map, self.origin, self.columns, self.rows, self.y_offset, self.x_offset = self.process(self.m_file)

        
    #Process the file to get the needed data. 
    def process(self, m_file):
       
        with open("mapmap.txt") as map_file:

            xy_flag = False
           
            for line in map_file:
               
                name_info = line.lstrip().rstrip().split(":")
         
                if name_info[0] == "width": cols = int(name_info[1]) #width of map
                
                elif name_info[0] == "height": rows = int(name_info[1]) #Height of map

                elif name_info[0] == "data": #Get all of the points in the map and format them in numpy
                   
                    raw_data = name_info[1].lstrip()[1:-1]
                    raw_data_list = map(str.strip, raw_data.strip().split(','))
                    pointer = 0
                    np_map = np.zeros([rows, cols], dtype=int)

                    for row in range(rows): 
                        for col in range(cols):
                         
                            np_map[row, col] = int(raw_data_list[pointer])
                            pointer += 1

                elif name_info[0] == "position": xy_flag = True #Set flag to get correct xy, instead of the orientation xy.

                elif xy_flag and name_info[0]=="x": xo = int(round(float(name_info[1]) * 20)) #set x offset

                elif xy_flag and name_info[0]=="y":
                 
                    yo = int(round(float(name_info[1]) * 20)) #set y offset
                    xy_flag = False #Set so we don't overwrite the correct xy
            
        np_map = np.flipud(np_map) #Flip it to set it up properly for the math implimented
        org = (-yo, -xo) #Set origin
        return np_map, org, cols, rows, yo, xo
   

    #Returns T/F for if the requested point is acceptable or not.
    def wantedPoint(self, point):
      
        return np.logical_and(self.getValue(point) >= 0, self.getValue(point) < self.th) #This is abnormal because numpy was having issues with the 0 < x < n being ambiguous


    #Get the value at the requested point
    def getValue(self, point):
       
        return self.Map[point]


    #Finds the closest free point to your requested point, using spiral pattern. https://stackoverflow.com/questions/398299/looping-in-a-spiral
    def closestPoint(self, point):
      
        row = col = 0
        d_row = 0
        d_col = -1

        for i in range(max(self.rows, self.columns)**2):
            if row == col or (row < 0 and row == -col) or (row > 0 and row == 1 - col):
            
                d_row, d_col = -d_col, d_row

            row, col = row + d_row, col + d_col
            new_row, new_col = point[0] + row, point[1] + col 
         
            #If the points are inbounds and its the correct value for the th then return these new points.
            if ((0 <= new_row < self.rows) and (0 <= new_col < self.columns)) and self.wantedPoint((new_row, new_col)): return (new_row, new_col)

    
    #Convert from RAS to Numpy
    def RAStoNumpy(self, point):
       
        return(point[1] - self.y_offset, point[0] - self.x_offset)


    #Convert from Numpy to RAS
    def NumpytoRAS(self, point):
       
        return (point[1] + self.x_offset, point[0] + self.y_offset)

                      
if __name__ == '__main__':
   
    try:
   
        map_file = "mapmap.txt" ### CHANGE WITH RAS DATA
        threshold = 75
        map = NewMap(map_file, threshold) 
        point = (58, 19) ###CHANGE WITH RAS DATA
        point = map.RAStoNumpy(point) 
        acceptable = map.wantedPoint(point)

        if not acceptable: point = map.closestPoint(point)

        point = map.NumpytoRAS(point) #Give back as something RAS can understand. 
        print(point)        

    except rospy.ROSInterruptException:

        rospy.loginfo("Exception thrown")
