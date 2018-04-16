#!/usr/bin/env python

#czy to kiedys zadziala?

import numpy as np
import rospy

from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from visualization_msg import Marker

pi = np.pi

global pub # publisher

def callback(data):
	pose = []
	pose.append(data.pose.position[0])
	pose.append(data.pose.position[1])
	pose.append(data.pose.position[2])
	
    marker = Marker()
    marker.header.frame_id = "/base_link"
    marker.header.stamp = rospy.Time.now()

    marker.ns = "basic_shapes"
    marker.id = 0

    marker.type = Marker.ARROW

    marker.action = Marker.ADD

    marker.pose.position.x = 0
    marker.pose.position.y = 0
    marker.pose.position.z = 0
	
	x = pose[0]
	y = pose[1]
	z = pose[2]
    marker.pose.orientation.x = 0
    marker.pose.orientation.y = np.sin(3.14/2)
    marker.pose.orientation.z = 0
    marker.pose.orientation.w = 1.0

    marker.scale.x = np.sqrt(x*x+y*y+z*z)
    marker.scale.y = 0.02
    marker.scale.z = 0.02

    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.color.a = 0.8
	
	
	pub.publish(marker)

def listener():
	rospy.init_node('RVIZ_MARKER', anonymous=False)
	rospy.Subscriber('nonkdl_pose', PoseStamped, callback)
	global pub 	
	pub = rospy.Publisher('nonkdl_marker', Marker, queue_size=10)

	#spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
	

if __name__ == '__main__':
	listener()





