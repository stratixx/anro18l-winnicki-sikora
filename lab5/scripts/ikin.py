#!/usr/bin/env python


import numpy as np
from scipy import optimize
import rospy
from math import *

from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
import robot

pi = np.pi	
th3 = 0
fps = 60#rospy.get_param('fps')
a2 = rospy.get_param('a2')
a3 = rospy.get_param('gripper')
bh = 0.3
z = 0.3
	

def callback(data):
	global last_res
	ointPose = data
	x = ointPose.pose.position.x
	y = ointPose.pose.position.y
	z = ointPose.pose.position.z
	a2 = rospy.get_param('a2')
	a3 = rospy.get_param('gripper')

	
	try:
		zz = z - bh
		t1 = atan2(y,x)
		h = pow((x/cos(t1)),2) + pow(zz,2)
		t2 = -atan2(zz*cos(t1),x) - acos((pow(a2,2) - pow(a3,2)+h)/(2*a2*pow(h,0.5)))
		t3 = acos((-pow(a2,2) - pow(a3,2) + h)/(2*a2*a3))	
		results = check_solution([t1, t2, t3], x, y, z)
		print(results[3])	
	except Exception:
		return
	"""
	#ograniczenia ruchu
	if t1 > 3.14 or t1 < -3.14:
		rospy.logerr("Zly kat")
		return
	
	if t2 > 0 or t2 < -1:
		rospy.logerr("Zly kat")
		return
	
	if t3 < 0 or t3 > 1.54:
		rospy.logerr("Zly kat")
		return
	"""
	robot.set_angles(t1, t2, t3)
	state = robot.get_joint_state(fps)	
	pub.publish(state)

def listener():
	# init node
	rospy.init_node('IKIN', anonymous=False)
	rospy.Subscriber('/pose_stamped', PoseStamped, callback)
	global pub 	
	pub = rospy.Publisher('/joint_states', JointState, queue_size = 30)
	robot.set_angles(0, 0, 0)
	state = robot.get_joint_state(fps)	
	pub.publish(state)

	rospy.spin()	
	
if __name__ == '__main__':
	robot = robot.Robot()
	listener()
