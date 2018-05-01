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
global robot # model robota

class JINT:

	def __init__(self):
		self.last_t = 1000
		self.last_params = np.matrix('0; 0; 0; 0; 0; 0')

	### interpolacja liniowa ###
	def linear_interpolation(self,x0, x1, t1, t):
		a = (x1 - x0)/(t1)	
		return x0 + a*t 

	### interpolacja splajnowa z dwoma funkcjami kwadratowymi ###
	def quad_spline_interpolation(self,x0, x1, t1, t):
		if self.last_t == (t - 1):
			params = self.last_params
		else:
			spline_array = np.array([[0, 0, 1, 0, 0, 0], 
						  [0, 0, 0, t1**2, t1, 1], 
						  [0, 1, 0, 0, 0, 0], 
						  [0, 0, 0, 2*t1, 1, 0], 
						  [(t1/2)**2, (t1/2), 1, -((t1/2)**2), -(t1/2), -1], 
						  [t1, 1, 0, -t1, -1, 0]])
			b = np.array([[x0],[x1],[0],[0],[0],[0]])
			params = np.linalg.solve(spline_array, b)
			params = params.tolist()
			self.last_params = params
		
		self.last_t = t
		print(params)
		if t < (t1/2):
			return params[0][0]*(t**2) + params[1][0]*t + params[2][0]
		else:
			return params[3][0]*(t**2) + params[4][0]*t + params[5][0]

	### interpolacja z trapezowym przebiegiem predkosci ###
	def trapezoid_vel_interpolation(self, x0, x1, t1, t):
		if self.last_t == (t - 1):
			params = self.last_params
		else:
			spline_array = np.array([[0, 0, 1, 0, 0, 0, 0, 0],
						  [0, 0, 0, 0, 0, t1**2, t1, 1],
						  [(t1**2)/25, t1/5, 1, -t1/5, -1, 0, 0, 0],
						  [0, 0, 0, 4*t1/5, 1, -(4*t1/5)**2, -4*(t1/5), -1],
						  [2*t1/5, 1, 0, -1, 0, 0, 0, 0],
						  [0, 0, 0, 1, 0, -8*t1/5, -1, 0],
						  [0, 1, 0, 0, 0, 0, 0, 0],
						  [0, 0, 0, 0, 0, 2*t1, 1, 0]])
			b = np.array([[x0],[x1],[0],[0],[0],[0],[0],[0]])
			params = np.linalg.solve(spline_array, b)
			params = params.tolist()
			self.last_params = params
			
		self.last_t = t
		print(params)
		if t < (t1/5):
			return params[0][0]*(t**2) + params[1][0]*t + params[2][0]
		if t >= t1/5 and t < (4*t1/5):
			return params[3][0]*t + params[4][0]
		else:
			return params[5][0]*(t**2) + params[6][0]*t + params[7][0]
		
	### wybranie odpowiedniego trybu interpolacji ###
	def interpole(self, type, x0, x1, t1, t):
		if type == 'linear':
			return self.linear_interpolation(x0, x1, t1, t)
		if type == 'quad_spline':
			return self.quad_spline_interpolation(x0, x1, t1, t)
		if type == 'trapezoid_vel':
			return self.trapezoid_vel_interpolation(x0, x1, t1, t)


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
	jint0 = JINT()
	jint1 = JINT()
	jint2 = JINT()
	while k <= samples:
		ang0 = jint0.interpole(req.interpolation_type, x[0], goal[0], samples, k)
		ang1 = jint1.interpole(req.interpolation_type, x[1], goal[1], samples, k)
		ang2 = jint2.interpole(req.interpolation_type, x[2], goal[2], samples, k)
		robot.set_angles(ang0, ang1, ang2)
		state = robot.get_joint_state(fps)
		pub = rospy.Publisher('joint_states', JointState, queue_size = 10)
		pub.publish(state)
		k = k + 1
		r.sleep()
				
	return InterpolationRequestResponse('done')

def jint_server():
	rospy.init_node('jint')
	s = rospy.Service('jint', InterpolationRequest, handle_interpolation_request)
	pub = rospy.Publisher('/joint_states', JointState, queue_size = 10)	
	init_state = robot.get_joint_state(0)	
	rospy.sleep(0.3)
	pub.publish(init_state)
	rospy.spin()

if __name__ == "__main__":
	# obiekt robota
	robot = robot.Robot()
	jint_server()
