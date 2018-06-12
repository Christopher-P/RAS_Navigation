#!/usr/bin/env python

'''
The idea of this is to let RAS know when he is localized or not. 
This is a service you want to call and return a T/F message. 
Currently having issues with tf not working to receive the information
for his current location. Going to try nested class.  
'''

import rospy, math, time, sys, os
from tf import TransformListener
from ras_msgs.srv import Localize


class Localize:
    def __init__(self):
        rospy.init_node('nav_test_localize2', anonymous=False)
        s = rospy.Service('localize', Localize, self.start_loc)
        rospy.loginfo("Reporting localized service")
        rospy.spin()
        rospy.on_shutdown(rospy.loginfo("Ending Service"))


    def start_loc(self, service_input):
        print(service_input)
        original = self.RAS()
        starting_pos = original.pos
        startimg_time = original.time
        loc = self.Local(starting_pos[0], starting_pos[1], starting_time) #set to now
        finished = False #are we localized?

        while not finished:
            current_RAS = self.RAS()
            current_pos = current_RAS.pos
            current_time = current_RAS.time
            loc.newLocal(current_pos[0], current_pos[1], current_time)
            dis = loc.getDistance()
            time_dif = loc.getTime()
            scale = 1/time_dif
            adjusted_dis = distance * scale
            if adjusted_dis > 10:
                rospy.loginfo("Localized, moving faster than 10m/s")
                print("Localized")
                finished = True
            else: 
                print("Not localized moving at", adjusted_dis, "m/s")


    def publishIt(self):
        pub = rospy.Publisher('localized', std_msgs.msg.String, queue_size=10)
        pub.publish(std_msgs.msg.String("True"))


    class Local:
        def __init__(self, x, y, t):
            self.current_local = self.last_local= (x, y)
            self.current_time = self.last_time = t


        def newLocal(self, x, y, t):
            self.last_local = self.current_local
            self.current_local = (x, y)
            self.last_time = self.current_time
            self.current_time = t


        def getDistance(self):
            x = self.current_local[0] - self.last_local[0]
            y = self.current_local[1] - self.last_local[1]
            return math.hypot(x, y)
        

        def getTime(self):
            if(self.current_time > self.last_time): #Should always be this way
                return self.current_time - self.last_time

            else:
                rospy.loginfo("Unexpected Time")
                return abs(self.current_time - self.last_time)


    class RAS:
        def __init__(self):
            self.tf = TransformListener()
            self.pos = self.getRAS()
            self.time = time.time()


        def getRAS(self):
            if self.tf.frameExists("/base_link") and self.tf.frameExists("/map"):
                t = self.tf.getLatestCommonTime("/base_link", "/map")
                pos, quat = self.tf.lookupTransform("/base_link", "/map", t)
                return(pos[0], pos[1]) # (x,y)




if __name__ == '__main__':
    try:
        Localize()
    except rospy.ROSInterruptException:
        rospy.loginfo("Exception thrown")