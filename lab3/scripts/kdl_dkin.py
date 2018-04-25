#!/usr/bin/env python

import rospy
import PyKDL
import numpy

pi = numpy.pi

from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped

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


def createFrame(base, a, d, al, th):
	pos = base.p + base.M*PyKDL.Vector(a,0,0)
	rot = base.M * PyKDL.Rotation.RPY(al, 0, 0)
	pos = pos + rot*PyKDL.Vector(0,0,d)
	rot = rot * PyKDL.Rotation.RPY(0,0,th)
	return PyKDL.Frame(rot,pos)


def callback(data):
	# pobierz wartosci katow w stawach
	joint = []
	joint.append(data.position[0])
	joint.append(data.position[1])
	joint.append(data.position[2])

	if joint[0] > 3.14 or joint[0] < -3.14:
		rospy.logerr("Zly kat")
		return
	
	if joint[1] > 0 or joint[1] < -1.54:
		rospy.logerr("Zly kat")
		return
	
	if joint[2] < 0 or joint[2] > 1.54:
		rospy.logerr("Zly kat")
		return

	robot = PyKDL.Chain()

	joint0 = PyKDL.Joint(PyKDL.Joint.RotZ)
	frame0 = createFrame(PyKDL.Frame(PyKDL.Vector(0,0,0)), a0, d1, al0, joint[0])
	segment0 = PyKDL.Segment(joint0, frame0)
	robot.addSegment(segment0)

	joint1 = PyKDL.Joint(PyKDL.Joint.RotZ)
	frame1 = createFrame(frame0, a1, d2, al1, joint[1])
	segment1 = PyKDL.Segment(joint1, frame1)
	robot.addSegment(segment1)

	joint2 = PyKDL.Joint(PyKDL.Joint.RotZ)
	frame2 = createFrame(frame1, a2, d3, al2, joint[2])
	segment2 = PyKDL.Segment(joint2, frame2)
	robot.addSegment(segment1)
	 
	solver = PyKDL.ChainFkSolverPos_recursive(robot)
	q = PyKDL.JntArray(robot.getNrOfJoints())
	q[0] = joint[0]
	q[1] = joint[1]
	q[2] = joint[2]

	wynik = PyKDL.Frame()
	boo = solver.JntToCart(q, wynik)

	pose = PoseStamped()
	pose.header.stamp = rospy.Time.now()
	pose.header.frame_id = "kdl"
	pose.pose.position.x = wynik.p.x()
	pose.pose.position.y = wynik.p.y()
	pose.pose.position.z = wynik.p.z()
	
	pub.publish(pose)
	print('Message')
	print(pose)


def listener():
	# init node
	rospy.init_node('KDL_DKIN', anonymous=False)
	rospy.Subscriber('joint_states', JointState, callback)
	global pub 	
	pub = rospy.Publisher('kdl_pose', PoseStamped, queue_size=10)

	rospy.spin()
	
if __name__ == '__main__':
	listener()
