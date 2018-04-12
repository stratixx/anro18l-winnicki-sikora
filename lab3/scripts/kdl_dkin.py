#!/usr/bin/env python

#czarek dzbanie nie sciagaj od nas XDDD

import rospy
import pyKDL

from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped

global th1, th2, th3 # katy w stawach
global a0, a1, a2, d1, d2, d3, al0, al1, al2 # parametry robota
global pub # publisher

# parametry robota
a0 = 0
a1 = 0
a2 = 0.5
d1 = 0
d2 = 0 
d3 = 0
al0 = 0
al1 = -pi/2
al2 = 0

global robot

def callback(data):
	#todo
	print('XD')



def listener():
	rospy.init_node('NONKDL_DKIN', anonymous=False)
	rospy.Subscriber('joint_states', JointState, callback)
	global pub 	
	pub = rospy.Publisher('nonkdl_pose', PoseStamped, queue_size=10)

	#spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
	

if __name__ == '__main__':
	listener()
