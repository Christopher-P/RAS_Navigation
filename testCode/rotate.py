#!/usr/bin/env python

'''
This program is designed to rotate RAS between two points.
First we put RAS at a (0,0) point and move the other point 
to match. Then find the angle and adjust based on the quad
it is in. From there we convert to Eurler then into quat
and give those angles to RAS to rotate. Right now he will
sometimes do full circles before facing the correct way.
I believe one cause maybe because he thinks he is in a 
spot he can't move to (wall). Only minor testing done,
however he faces the right direction. 
'''

import rospy, math
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
#from actionlib_msgs.msg import *  #I don't think we need this, if any errors pring it back up.
from ras_msgs.srv import Rotate
#from tf.msg import tfMessage #I don't think we need this, if any errors pring it back up.
from tf.transformations import quaternion_from_euler
from tf.transformations import quaternion_multiply


def rotate_robot(points):
	   
    #original points.
    x = points.x1
    y = points.y1
    x2 = points.x2
    y2 = points.y2

    #Normalize it.
    x2 = x2 - x
    y2 = y2 - y
    x = y = 0

    #Determine the quad.
    if x2 < 0 and y2 < 0: quad = 3
    elif x2 < 0: quad = 2
    elif y2 < 0: quad = 4
    else: quad = 1

    #Do some math.
    theta = get_theta(quad, abs(x2), abs(y2)) #Get angle, rads.
    deg = theta * (180/math.pi)
    q_orgin = quaternion_from_euler(0, 0, 0) #Set him to the original.
    q_rot = quaternion_from_euler(theta, 0, 0) #Set new one. 
    q_new = quaternion_multiply(q_rot, q_orgin) #Do some kind of math magic.

    #tell the action client that we want to spin a thread by default.
    move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
    rospy.loginfo("wait for the action server to come up")

    #allow up to 5 seconds for the action server to come up.
    move_base.wait_for_server(rospy.Duration(5))

    #we'll send a goal to the robot to move 3 meters forward.
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()

    #Rotate/Pose.
    goal.target_pose.pose.orientation.x = q_new[2]
    goal.target_pose.pose.orientation.y = q_new[1]
    goal.target_pose.pose.orientation.z = q_new[0]
    goal.target_pose.pose.orientation.w = q_new[3]
    goal.target_pose.pose.position.x = 0.0
    goal.target_pose.pose.position.y = 0.0
    goal.target_pose.pose.position.z = 0.0
    
    #Start moving.
    move_base.send_goal(goal)

    #allow TurtleBot up to 60 seconds to complete task.
    success = move_base.wait_for_result(rospy.Duration(60)) 

    if not success:

        move_base.cancel_goal()
        rospy.loginfo("The base failed to rotate for some reason")
        return "Failure" 

    else:

        # We made it!
        state = move_base.get_state()
        if state == GoalStatus.SUCCEEDED:
            rospy.loginfo("Hooray, the base rotated")
        return "Success"
     

#We will be geting angle based on the quad.
def get_theta(quad, x2, y2):

    theta = 0

    if quad == 1:
        
        theta = math.atan(y2/x2) #No adjustment for Q1.
       
    elif quad == 2 or quad == 4:
        
        theta = math.atan(x2/y2)

        if quad == 2: 
            theta = theta + 1.5707963268 #Adjust for being in Q2, pi/2.
        
        else:
            theta = theta + 4.7123889804 #Adjust for being in Q4 2pi.

    elif quad == 3:
        
        c = math.sqrt(math.pow(2, x2) + math.pow(2, y2))
        theta = math.acos(x2/c)
        theta = theta + 3.1415926536 #Adjust for Q3 2/3pi.
      
    return theta


#Service start up.
class RotateToObject():

    def __init__(self):

        rospy.init_node('nav_test_rotate', anonymous=False)
    	s = rospy.Service('rotate', Rotate, rotate_robot)
    	rospy.loginfo("Beginning rotate service")
    	rospy.spin()

    	#what to do if shut down (e.g. ctrl + C or failure).
    	rospy.on_shutdown(self.shutdown)


    def shutdown(self):

        rospy.loginfo("Editing Service")


if __name__ == '__main__':

    try:

        RotateToObject()

    except rospy.ROSInterruptException:
        
        rospy.loginfo("Exception thrown")
