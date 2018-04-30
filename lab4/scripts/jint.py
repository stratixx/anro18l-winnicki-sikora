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
global fps
fps = rospy.get_param('fps')

global pub # publisher
global robot


def linear_interpolation(x0, x1, t1, t):
	a = (x1 - x0)/(t1)	
	return x0 + a*t 



def interpole(type, x0, x1, t1, t):
	if type == 'linear':
		return linear_interpolation(x0, x1, t1, t)


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


	#sprawdzenie poprawnosci katow
	if goal[0] > 3.14 or goal[0] < -3.14:
		rospy.logerr("Zly kat")
		return InterpolationRequestResponse("Invalid goal for joint0")
	
	if goal[1] > 0 or goal[1] < -1.54:
		rospy.logerr("Zly kat")
		return InterpolationRequestResponse("Invalid goal for joint1")
	
	if goal[2] < 0 or goal[2] > 1.54:
		rospy.logerr("Zly kat")
		return InterpolationRequestResponse("Invalid goal for joint2")
	 
	# katy poczatkowe
	x = [0.0, 0.0, 0.0]
	x[0] = robot.joint_position[0]
	x[1] = robot.joint_position[1]
	x[2] = robot.joint_position[2]
	
	r = rospy.Rate(fps)
	k = 0 # poczatkowy czas dyskretny
	while k <= samples:
		ang0 = interpole(req.interpolation_type, x[0], goal[0], samples, k)
		ang1 = interpole(req.interpolation_type, x[1], goal[1], samples, k)
		ang2 = interpole(req.interpolation_type, x[2], goal[2], samples, k)
		robot.set_angles(ang0, ang1, ang2)
		state = robot.get_joint_state(fps)
		pub = rospy.Publisher('joint_states', JointState, queue_size = 10)
		pub.publish(state)
		k = k + 1
		print(state)
		#print(k)
		#print(ang0)
		#print(ang1)
		#print(ang2)
		#print('---')
		r.sleep()
				
	return InterpolationRequestResponse('done')

def jint_server():
	rospy.init_node('jint')
	s = rospy.Service('jint', InterpolationRequest, handle_interpolation_request)
	pub = rospy.Publisher('/joint_states', JointState, queue_size = 10)	
	init_state = robot.get_joint_state(0)	
	rospy.sleep(3)
	pub.publish(init_state)
	rospy.spin()

if __name__ == "__main__":
	# obiekt robota
	robot = robot.Robot()
	jint_server()
