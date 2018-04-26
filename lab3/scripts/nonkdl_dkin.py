#!/usr/bin/env python

#czarek dzbanie nie sciagaj od nas XDDD

import numpy as np
import rospy
import math

from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from tf.transformations import quaternion_from_euler

pi = np.pi

global th1, th2, th3 # katy w stawach
global a0, a1, a2, d1, d2, d3, al0, al1, al2 # parametry robota
global pub # publisher

#wysokosc bazy
base_height=rospy.get_param('base_height')

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

global robot

# obiekt robota
robot = []

staw1 = [a0, d1, al0, 0]
staw2 = [a1, d2, al1, 0]
staw3 = [a2, d3, al2, 0]

robot.append(staw1)
robot.append(staw2)
robot.append(staw3)



def ROTZ(theta):
	A = np.array([[np.cos(theta), -np.sin(theta), 0, 0], [np.sin(theta), np.cos(theta), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
	return A

def TRANSX(a):
	A = np.array([[1, 0, 0, a], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
	return A

def ROTX(alpha):
	A = np.array([[1, 0, 0, 0], [0, np.cos(alpha), -np.sin(alpha), 0], [0, np.sin(alpha), np.cos(alpha), 0], [0, 0, 0, 1]])
	return A

def TRANSZ(d):
	A = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, d], [0, 0, 0, 1]])
	return A



def callback(data):
	# pobierz wartosci katow w stawach
	joint = []
	joint.append(data.position[0])
	joint.append(data.position[1])
	joint.append(data.position[2])

	robot[0][3] = joint[0]
	robot[1][3] = joint[1]
	robot[2][3] = joint[2]
	
	if joint[0] > 3.14 or joint[0] < -3.14:
		rospy.logerr("Zly kat")
		return
	
	if joint[1] > 0 or joint[1] < -1.54:
		rospy.logerr("Zly kat")
		return
	
	if joint[2] < 0 or joint[2] > 1.54:
		rospy.logerr("Zly kat")
		return
	
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
	KIN = KIN1_2
	
	# obliczenie pozycji koncowki	
	pos_zero = np.array([0, 0, 0, 1]).transpose()
	pos = np.dot(KIN, pos_zero)
	

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

	quat = quaternion_from_euler (r, p,y)
	pose.pose.orientation.x = quat[0]
	pose.pose.orientation.y = quat[1]
	pose.pose.orientation.z = quat[2]
	pose.pose.orientation.w = quat[3]
	
	
	pub.publish(pose)
	#print('Message')
	print(pose)

def listener():
	rospy.init_node('NONKDL_DKIN', anonymous=False)
	rospy.Subscriber('joint_states', JointState, callback)
	global pub 	
	pub = rospy.Publisher('nonkdl_pose', PoseStamped, queue_size=10)

	#spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
	

if __name__ == '__main__':
	listener()





