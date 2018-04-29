#!/usr/bin/env python


import numpy as np
import rospy
import math

from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from tf.transformations import quaternion_from_euler
from lab4.srv import *
import robot

pi = np.pi
fps = 30

global pub # publisher

# obiekt robota
robot = robot.Robot()

def basic_interpolation(x0, x1, t1, t):
	a = (x1 - x0)/(t1)	
	return x0 + a*t 

def handle_interpolation_request(req):
	# sprawdzenie poprawnosci zadania
	int_time = req.time
	if int_time <= 0:
		return InterpolationRequestResponse("Invalid time")

	# przejscie na  czas dyskrenty
	samples = fps*int_time	
	if samples <= 0:
		return InterpolationRequestResponse("Invalid time")

	# cel interpolacji
	goal = [0.0, 0.0, 0.0]
	goal[0] = req.angle0
	goal[1] = req.angle1
	goal[2] = req.angle2
	 
	# katy poczatkowe
	x = [0.0, 0.0, 0.0]
	x[0] = robot.joint_position[0]
	x[1] = robot.joint_position[1]
	x[2] = robot.joint_position[2]
	
	r = rospy.Rate(fps)
	k = 0 # poczatkowy czas dyskretny
	while k < samples:
		dst0 = basic_interpolation(x[0], goal[0], samples, k)
		dst1 = basic_interpolation(x[1], goal[1], samples, k)
		dst2 = basic_interpolation(x[2], goal[2], samples, k)
		pose = robot.createPose(dst0, dst1, dst2)
		pub = rospy.Publisher('joint_states', PoseStamped, queue_size = 10)
		pub.publish(pose)
		k = k + 1
		print(k)
		print(dst0)
		print(dst1)
		print(dst2)
		print('---')
		r.sleep()
				

	return InterpolationRequestResponse('done')

def jint_server():
	rospy.init_node('jint')
	s = rospy.Service('jint', InterpolationRequest, handle_interpolation_request)
	pub = rospy.Publisher('joint_states', PoseStamped, queue_size = 10)
	rospy.spin()

if __name__ == "__main__":
	jint_server()
