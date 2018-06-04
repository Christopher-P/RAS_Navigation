#!/usr/bin/env python

'''
Get human location from rostopic (Sim for now)
Get RAS location from rostopic (tf tree)
Do math to leave 2 foot space between RAS and human
Call goto_xy service
Return good debugging messages
'''

import rospy
# from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
# import actionlib
# from actionlib_msgs.msg import *
# from ras_msgs.srv import Goto_human
from ras_msgs.srv import Goto_xy


class GoToHuman():
    def __init__(self):
        rospy.init_node('nav_test', anonymous=False)

       

        #Get human from publication
        Human_loc = (4.5, 2.3)
        h_x = Human_loc[0]
        h_y = Human_loc[1]

        #Get robit from publication
        RAS_loc = (0.0, 0.0)
        r_x = RAS_loc[0]
        r_y = RAS_loc[1]

        #Do math, given location A and B, straight line between the two with 2ft gap between
        rospy.wait_for_service('goto_xy')
        goto_human = rospy.ServiceProxy('goto_xy', Goto_xy)


        if ((h_x == r_x) or (h_y == r_y)):
            print ("There's a straight horizontal")
            # Simple -- Just keep it two feet away
            if (h_x == r_x): #horizontal match, change this to be more forgiving with in 5 degrees?
                #rosservice call goto_xy h_x, h_y-0.6096
                horizontal = goto_human(h_x, h_y-0.6096)
                return horizontal.response
            else:
                goto(h_x-0.6096, h_y) #vertical  match, change this to be more forgiving with in 5 degrees?
                #rosservice call goto_xy h_x-0.6096, h_y
                vert = goto_human(h_x-0.6096, h_y)
                return triangle.response

        else:
            # triangle -- equalatiral triangle with 0.6096m (2ft) longest size 
            # and the legs would be 0.431m (1.41ft) each.
            #rosservice call goto_xy h_x-0.431, h_y-0.431
            triangle = goto_human(h_x-0.431, h_y-0.431)
            return triangle.response

        

        #log stuff
    	rospy.loginfo("Beginning goto_human service")
    	rospy.spin()

    	#what to do if shut down (e.g. ctrl + C or failure)
    	rospy.on_shutdown(self.shutdown)

    

    def shutdown(self): 
        rospy.loginfo("Editing Service")


if __name__ == '__main__':
    try:
        GoToHuman() #this returns the response not sure what to do with it right now

    except rospy.ROSInterruptException:
        rospy.loginfo("Exception thrown")

