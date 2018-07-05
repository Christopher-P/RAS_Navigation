#!/usr/bin/env python


'''
This program is designed to listen to the lurking ai (name to be changed)
and go to the position it predicts is the correct place to sit and wait. 
Untested. 
'''


import rospy
from ras_msgs.srv import Lurker_base_srv, Goto_xy


#Listening for the move command until it's triggered then move it.
def lurker_move(data):

    rospy.init_node('Listening for base move') #Start listening for xy of where RAS should wait.
    rospy.Subscriber("lurking_ai", String, move_it) # Nothing something we can currently listen for, get correct name from Yulia.
    rospy.spin() 


#Move the base after it is triggered
def move_it(data):

    rospy.wait_for_service('goto_xy') #wait for service to start, need to start yourself (run file).
    goto_place = rospy.ServiceProxy('goto_xy', Goto_xy) 
    moved = goto_place(data.x, data.y) #Move to the recommended location. 
    rospy.loginfo(moved.response)
    return moved.response
     

#Start services
class LurkerBase():

    def __init__(self):

        rospy.init_node('move_lurking_base', anonymous=False)
    	s = rospy.Service('Lurker_base_srv', Lurker_base_srv, lurker_move) #Start service.
    	rospy.loginfo("Beginning lurker base move service")
    	rospy.spin()

    	#what to do if shut down (e.g. ctrl + C or failure)
    	rospy.on_shutdown(self.shutdown)


    def shutdown(self):

        rospy.loginfo("Ending Lurker Base Service")


if __name__ == '__main__':

    try:

        LurkerBase()
    
    except rospy.ROSInterruptException:

        rospy.loginfo("Exception thrown")