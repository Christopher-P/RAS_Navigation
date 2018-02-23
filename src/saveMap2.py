#!/usr/bin/env python
"""
Save the map every so many seconds
"""
import time
from datetime import datetime
import rospy
from cartographer_ros_msgs.srv import WriteState

def saveMap(nowTime, path, filename):
    rospy.wait_for_service("write_state")

    try:
        #Save to current working directory
        write = rospy.ServiceProxy("write_state", WriteState)
        #write(path + filename)
        #Save to map storage directory
        newPath = path + "old_maps/" + str(nowTime) + ".pbstream"
        write(newPath)
    except rospy.ServiceException, e:
        rospy.roserr("Service call failed: %s" % e)

if __name__ == "__main__":
    nowTime = datetime.now().time()
    rospy.init_node('saveMap')
    filename = rospy.get_param("~filename", None)
    path = rospy.get_param("~path", None)

    print(path + filename)

    if not filename:
        rospy.loger("File path to save map is required!")

    while not rospy.is_shutdown():
        time.sleep(30)
        saveMap(nowTime, path, filename)
        rospy.loginfo("Saved map")
