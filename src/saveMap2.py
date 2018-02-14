#!/usr/bin/env python
"""
Save the map every so many seconds
"""
import time
import rospy
from cartographer_ros_msgs.srv import WriteState

def saveMap(filename):
    rospy.wait_for_service("write_state")

    try:
        write = rospy.ServiceProxy("write_state", WriteState)
        write(filename)
    except rospy.ServiceException, e:
        rospy.roserr("Service call failed: %s" % e)

if __name__ == "__main__":
    rospy.init_node('saveMap')
    filename = rospy.get_param("~filename", None)

    if not filename:
        rospy.logerr("File path to save map is required!")

    while not rospy.is_shutdown():
        time.sleep(30)
        saveMap(filename)
        rospy.loginfo("Saved map")
