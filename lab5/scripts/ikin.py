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
	x = ointPose.pose.position.x
	z = ointPose.pose.position.z
	y = ointPose.pose.position.y
	a2 = rospy.get_param('a2')
	a3 = rospy.get_param('gripper')
	
	normxy = np.sqrt(x*x+y*y)

	ang1 = np.arctan2(y/normxy,x/normxy) # To chyba nawet dziala
	ang2 = 0
	ang3 = 0

	#sumAng23 = np.arcsin(-z/(a2+a3))
	#ang1 = np.arccos( x/( (a3+a2)*np.cos(sumAng23) ) )
	#ang2 = sumAng23-0.0
	#ang3 = 0.0
	
	#sprawdzenie poprawnosci katow
	if ang1 > pi or ang1 < -pi:
		rospy.logerr("Zly kat")
		raise Exception
	
	if ang2 > 0 or ang2 < -pi/2:
		rospy.logerr("Zly kat")
		raise Exception
	
	if ang3 < 0 or ang3 > pi/2:
		rospy.logerr("Zly kat")
		raise Exception		

	robot.set_angles(ang1, ang2, ang3)
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
