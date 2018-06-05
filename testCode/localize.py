#!/usr/bin/env python



import rospy, math, time, sys, os
from tf import TransformListener
from ras_msgs.srv import Localize


#Localize class to find information between two points
class Localize():

    def __init__(self, x, y, t): #Constructor
        self.current_local = (x, y)
        self.last_local = (x, y)
        self.current_time = t
        self.last_time = t


    def newLocation(self, x, y, t): #set a new location, update old location
        self.last_local = self.current_local
        self.current_local = (x, y)
        self.last_time = self.current_time
        self.current_time = t



    def getDistance(self): #distance between two points
        x = self.current_local[0]-self.last_local[0]
        y = self.current_local[1]-self.last_local[1]
        return math.hypot(x, y)


    def getTime(self):
        if (self.current_time > self.last_time): #Should also be the case, moving forward in time
            return self.current_time - self.last_time
        
        else: 
            rospy.loginfo("Unexpected Time")
            return abs(self.current_time - self.last_time)


#Information needed from RAS a particular moment in time
#Still need to get time information
class RAS():

    def __init__(self):
        self.tf = TransformListener()
        self.pos, self.time = self.getRAS()

    def getRAS(self):
        #Time reasoning, I am going to grab the time at the same moment I'm asking RAS where it is located
        #This way we're not relying on RAS' clock to be correct constantly. It should be indepdent of that
        #Same as in goto_human
        if self.tf.frameExists("/base_link") and self.tf.frameExists("/map"):
            t = self.tf.getLatestCommonTime("/base_link", "/map")
            position, quaternion = self.tf.lookupTransform("/base_link", "/map", t) 
            return (position, time.time())
    
    def getValues(self):
        return (self.pos, self.time)



def publish_localizing(notinput):
    pub = rospy.Publisher('localized', std_msgs.msg.String, queue_size=10)
    pub.publish(std_msgs.msg.String("True"))


if __name__ == '__main__':
   
    try: 
        original = RAS() #Get original RAS location
        starting_pos, starting_time = original.getValues()
        local = Localize(starting_pos[0], starting_pos[1], starting_time) #set the local position to this thing and time
        finished = False 

        while not finished: #While we're not localized
            current_RAS = RAS() #Get the current RAS location
            current_pos, current_time = current_RAS.getValues()
            local.newLocation(current_pos[0], current_pos[1], current_time) #set this new location and time 
            distance = local.getDistance() #distance between the two points
            time_difference = local.getTime()
            #Need to get distance/second, we need at least 10 meters per second
            scale = 1/time_difference #Scale to get to standard second
            adjusted_distance = distance * scale #scale up/down the meters to be adjusted to x meters/ 1 second
            if adjusted_distance > 10: 
                rospy.loginfo("Localized, moving faster than 10m/s")
                finished = True
        
        #Service Stuff
        rospy.init_node('nav_test_localize', anonymous=False)
    	s = rospy.Service('localize', Localize, publish_localizing)
    	rospy.loginfo("Reporting localized service")
    	rospy.spin()
        rospy.on_shutdown(rospy.loginfo("Ending Service"))


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(e)

    except rospy.ROSInterruptException:
        rospy.loginfo("Exception thrown")
