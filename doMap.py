#!/usr/bin/env python

from nav_msgs.msg import *
from nav_msgs.srv import *
from std_msgs.msg import *

import rospy

mapp = ""

def callback(data):
    global mapp 
    mapp = data

def returnMap(req):
    global mapp
    return GetMapResponse(mapp)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=False)

    rospy.Subscriber("/map", OccupancyGrid, callback)

    s = rospy.Service('GetMap', "map", returnMap)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == "__main__":
    listener()

