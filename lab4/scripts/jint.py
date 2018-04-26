#!/usr/bin/env python


import numpy as np
import rospy
import math

from nonkdl_dkin import ROTZ, ROTX, TRANSZ, TRANSX
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from tf.transformations import quaternion_from_euler
from lab4.srv import *

pi = np.pi
fps = 30

global a0, a1, a2, d1, d2, d3, al0, al1, al2 # parametry robota
global pub # publisher

#wysokosc bazy
base_height=rospy.get_param('base_height')
gripper=rospy.get_param('gripper')

# parametry robota
a0 = rospy.get_param('a0')
a1 = rospy.get_param('a1')
a2 = rospy.get_param('a2') 
d1 = rospy.get_param('d1') + base_height
d2 = rospy.get_param('d2') 
d3 = rospy.get_param('d3') 
al0 = rospy.get_param('al0')
al1 = rospy.get_param('al1')
al2 = rospy.get_param('al2')

#obiekt robota
robot = []

staw1 = [a0, d1, al0, 0]
staw2 = [a1, d2, al1, 0]
staw3 = [a2, d3, al2, 0]
staw4 = [gripper, 0, 0, 0]

robot.append(staw1)
robot.append(staw2)
robot.append(staw3)
robot.append(staw4)

global joint

joint = [0.00, 0.00, 0.00] # bazowe polozenie robota

def createPose():
	robot[0][3] = joint[0]
	robot[1][3] = joint[1]
	robot[2][3] = joint[2]
	
	#sprawdzenie poprawnosci katow
	if joint[0] > 3.14 or joint[0] < -3.14:
		rospy.logerr("Zly kat")
		return
	
	if joint[1] > 0 or joint[1] < -1.54:
		rospy.logerr("Zly kat")
		return
	
	if joint[2] < 0 or joint[2] > 1.54:
		rospy.logerr("Zly kat")
		return

	#tablica macierzy
	joints = []
	
	# obliczenie macierzy zlacz
	for staw in robot:
		R1 = ROTX(staw[2])
		R2 = TRANSX(staw[0])
		R3 = ROTZ(staw[3])
		R4 = TRANSZ(staw[1])
		R = np.dot(R1,R2)
		R = np.dot(R, R3)
		R = np.dot(R, R4)
		joints.append(R)
	
	# obliczenie kinematyki prostej
	KIN0_1 = np.dot(joints[0],joints[1])
	KIN1_2 = np.dot(KIN0_1, joints[2])
	KIN2_3 = np.dot(KIN1_2, joints[3])
	KIN = KIN2_3
	
	# obliczenie pozycji koncowki	
	pos_zero = np.array([0, 0, 0, 1]).transpose()
	pos = np.dot(KIN, pos_zero)
	
	#generacja pozycji
	pose = PoseStamped()
	pose.header.stamp = rospy.Time.now()
	pose.header.frame_id = "base_link"

	# przesuniecie poczatku wektora nad baze	
	pose.pose.position.x = np.take(KIN, [3])
	pose.pose.position.y = np.take(KIN, [7])
	pose.pose.position.z = np.take(KIN, [11])
	
	#obliczenie katow rpy
	r11 = np.take(KIN, [0])
	r21 = np.take(KIN, [4])
	r31 = np.take(KIN, [8])
	r32 = np.take(KIN, [9])
	r33 = np.take(KIN, [10])
					
	r = math.atan2(r32, r33)
	p = math.atan2(-r31, math.sqrt(r32 ** 2 + r33 ** 2))
	y = math.atan2(r21, r11)
	
	# obliczenie kwaternionu
	quat = quaternion_from_euler (r, p,y)
	pose.pose.orientation.x = quat[0]
	pose.pose.orientation.y = quat[1]
	pose.pose.orientation.z = quat[2]
	pose.pose.orientation.w = quat[3]
	
	return pose

def interpolation(x0, x1, t1, t):
	a = (x1 - x0)*(t1)	
	return x0 + a*t 

def findJointName(num):
	if num == 0:
		return "base_link_to_segment_1_joint_continuous"
	if num == 1:
		return "segment_1_to_segment_2_joint_continuous"
	if num == 2:
		return "segment_2_to_gripper_joint_continuous"
	else:
		raise Exception


def handle_interpolation_request(req):
	# sprawdzenie poprawnosci zadania
	which_one = req.joint
	if which_one > 2 or which_one < 0:
		return InterpolationRequestResponse("Joint does not exist")
	int_time = req.time

	if int_time <= 0:
		return InterpolationRequestResponse("Invalid time")
	# przejscie na  czas dyskrenty
	samples = fps*int_time	
	if samples <= 0:
		return InterpolationRequestResponse("Invalid time")
	try:
		name = findJointName(which_one)
	except Exception:
		return InterpolationRequestResponse("Joint does not exist")

	#parametry interpolacji
	x0 = joint[which_one]
	dst = x0 + req.angle
	s = 0
	rate = rospy.Rate(fps)
	while True:
		lin_angle = interpolation(x0, angle + x0, samples, s)
		joint[which_one] = lin_angle
		pose = createPose()
		pub.publish(pose)
	

def jint_server():
	rospy.init_node('jint')
	s = rospy.Service('jint', InterpolationRequest, handle_interpolation_request)
	pub = rospy.Publisher('joint_states', PoseStamped, queue_size = 10)
	rospy.spin()

if __name__ == "__main__":
	jint_server()
