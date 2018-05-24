#!/usr/bin/env python


import numpy as np
import rospy
import math

from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
import robot

pi = np.pi

global pub
global robot # model robota
global fps
fps = rospy.get_param('fps')


def callback(data):
	ointPose = data
	print('hello from callback')
	


	ang0 = 1.0
	ang1 = 1.0
	ang2 = 1.0
	robot.set_angles(ang0, ang1, ang2)
	state = robot.get_joint_state(fps)
	pub.publish(state)

def listener():
	# init node
	rospy.init_node('IKIN', anonymous=False)
	rospy.Subscriber('/pose_stamped', PoseStamped, callback)
	global pub 	
	pub = rospy.Publisher('/joint_states', JointState, queue_size = 30)	

	rospy.spin()
	
if __name__ == '__main__':
	robot = robot.Robot()
	listener()
