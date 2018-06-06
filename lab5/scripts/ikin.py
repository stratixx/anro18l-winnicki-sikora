#!/usr/bin/env python


import numpy as np
from scipy.optimize import 
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

a2 = 0.4
a3 = 0.1
bh = 0.3

class Result:
	def __init__(self, t1, t2 ,t3):
		self.t1 = t1
		self.t2 = t2
		self.t3 = t3

def fun_z(th2):
	return z - bh + a2*sin(th2) + a3*sin(th2 + th3)

def th1_cos(x, t2, t3):
	return acos(x/(a2*cos(t2) + a3*cos(t2 + t3)))

def th1_sin(y, t2, t3):
	return asin(y/(a2*cos(t2) + a3*cos(t2 + t3)))


def callback(data):
	ointPose = data
	x = ointPose.pose.position.x
	z = ointPose.pose.position.z
	y = ointPose.pose.position.y
	a2 = rospy.get_param('a2')
	a3 = rospy.get_param('gripper')
	
	t3_d = np.linspace(0, np.pi/2, num=100)
	sol = np.zeros(100)

	results = []

	i = 0
	while i < 100:
		th3 = t3_d[i]
		tmp = optimize.root(fun_z, 0)
		sol[i] = tmp.x
	
		try:
			t1c= th1_cos(x, sol[i], t3_d[i])
			t1s= th1_sin(y, sol[i], t3_d[i])	
			if(t1c - t1s > 0.001):
				i = i + 1
				continue
		except ValueError:
			t1c = 1000
			t1s = 1000
			i = i + 1
			continue

		#sprawdzenie poprawnosci katow
		if t1c > pi or t1c < -pi:
			rospy.logerr("Zly kat")
			raise Exception
	
		if sol[i] > 0 or sol[i] < -pi/2:
			rospy.logerr("Zly kat")
			raise Exception
	
		if t3_d[i] < 0 or t3_d[i] > pi/2:
			rospy.logerr("Zly kat")
			raise Exception	

		res = Result(t1c, sol[i], t3_d[i])
		print(res.t1)
		print(res.t2)
		print(res.t3)
		results.append(res)
	



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
