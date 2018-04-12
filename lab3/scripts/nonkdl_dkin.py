#!/usr/bin/env python

#czarek dzbanie nie sciagaj od nas XDDD

import numpy as np
import rospy

from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped

pi = np.pi

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
	KIN = np.dot(joints[0],joints[1])
	KIN = np.dot(KIN, joints[2])
	print('KIN')
	print(KIN)
	
	# obliczenie pozycji koncowki	
	pos_zero = np.array([0, 0, 0, 1]).transpose()
	pos = np.dot(KIN, pos_zero)
	print('POS')
	print(pos)
	
	pose = PoseStamped()
	pose.header.stamp = rospy.Time.now()
	pose.header.frame_id = "nonkdl"
	pose.pose.position.x = pos[0]
	pose.pose.position.y = pos[1]
	pose.pose.position.z = pos[2]
	
	pub.publish(pose)
	print('Message')
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





