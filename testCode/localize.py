#!/usr/bin/env python


import rospy, collections, math, time, sys, os
from tf import TransformListener

#Localize class to find information between two points
class Localize():

    def __init__(self, x, y, time): #Constructor
        self.current_local = (x, y)
        self.last_local = (x, y)
        self.current_time = time
        self.last_time = time


    def newLocation(self, x, y, time): #set a new location, update old location
        self.last_local = self.current_local
        self.current_local = (x, y)
        self.last_time = self.current_time
        self.current_time = time


    def getDistance(self): #distance between two points
        x = self.current_local[0]-self.last_local[0]
        y = self.current_local[1]-self.last_local[1]
        return math.hypot(x, y)


#Information needed from RAS a particular moment in time
#Still need to get time information
class RAS():

    def __init__(self):
        self.tf = TransformListener()
        self.pos = self.getRAS()
        self.time = 1

    def getRAS(self): #get data from tf listener
        #returning dummy numbers until we can use RAS
        # if self.tf.frameExists("/base_link") and self.tf.frameExists("/map"):
        #     t = self.tf.getLatestCommonTime("/base_link", "/map")
        #     position, quaternion = self.tf.lookupTransform("/base_link", "/map", t) #position is tuple (x, y, z), quat (x, y, z, w)
        return (0.0, 0.0, 0.0)
            # return (0, 0, 0)
    
    def getPos(self):
        return self.pos

if __name__ == '__main__':
    try: 
        original = RAS() #Get original RAS location
        startPos = original.getPos()
        local = Localize(startPos[0], startPos[1], 1) #set the local position to this thing and time
        finished = False #Have we been localized?

        while not finished: #While we're not localized
            currentRAS = RAS() #Get the current RAS location
            currentPos = currentRAS.getPos()
            # local.newLocation(currentPOS[0], currentPOS[1]) #set this new location 
            local.newLocation(0, 0.23, 1) #dummy values for now
            distance = local.getDistance() #distance between the two points
            if distance > 1: finished = True #It was greater than a meter, still need to include a time check
            else: finished = True #For now while I'm testing this out
            time.sleep(0.1)


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(e)
#     # except rospy.ROSInterruptException:
#     #     rospy.loginfo("Exception thrown")
