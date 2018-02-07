#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import PoseStamped
import std_msgs.msg
import geometry_msgs.msg

def talker():

    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
    rospy.init_node('RASbot')

    h = std_msgs.msg.Header()
    h.stamp = rospy.Time.now()
    h.frame_id = "map"

    p = geometry_msgs.msg.Pose()
    p.position.x = 0.236744120717
    p.position.y = 0.00946978013963
    p.position.z = 0.0

    p.orientation.x = 0.0
    p.orientation.y = 0.0
    p.orientation.z = 185563380068
    p.orientation.w = 0.982632297443

    go = PoseStamped()
    go.header = h
    go.pose = p
    
    rospy.loginfo(go)
    pub.publish(go)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
