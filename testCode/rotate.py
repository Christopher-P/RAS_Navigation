#!/usr/bin/env python

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from ras_msgs.srv import Rotate

def rotate_robot(notinput):
    #tell the action client that we want to spin a thread by default
    move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
    rospy.loginfo("wait for the action server to come up")
    #allow up to 5 seconds for the action server to come up
    move_base.wait_for_server(rospy.Duration(5))

    #we'll send a goal to the robot to move 3 meters forward
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.orientation.w = notinput.w #Rotate

    #start moving
    move_base.send_goal(goal)

    #allow TurtleBot up to 60 seconds to complete task
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
        


class RotateToObject():
    def __init__(self):
        rospy.init_node('nav_test_rotate', anonymous=False)
    	s = rospy.Service('rotate', Rotate, rotate_robot)
    	rospy.loginfo("Beginning rotate service")
    	rospy.spin()

    	#what to do if shut down (e.g. ctrl + C or failure)
    	rospy.on_shutdown(self.shutdown)

    

    def shutdown(self):
        rospy.loginfo("Editing Service")


if __name__ == '__main__':
    try:
        RotateToObject()
    except rospy.ROSInterruptException:
        rospy.loginfo("Exception thrown")

