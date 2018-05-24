#!/usr/bin/env python


import numpy as np
import rospy
import math

from geometry_msgs.msg import PoseStamped
from tf.transformations import quaternion_from_euler
from lab4.srv import *
from interpolators import JINT

pi = np.pi

global fps
fps = rospy.get_param('fps')

global pub # publisher
global act_position
global act_orientation


def create_pose():
	global act_position
	global act_orientation
	pose = PoseStamped()

	#header
	pose.header.stamp = rospy.Time.now()
	pose.header.frame_id = 'base_link'

	#pose.position
	pose.pose.position.x = act_position[0]
	pose.pose.position.y = act_position[1]
	pose.pose.position.z = act_position[2]

	#pose.orientation
	quat = quaternion_from_euler(act_orientation[0], act_orientation[1], act_orientation[2])
	pose.pose.orientation.x = quat[0]
	pose.pose.orientation.y = quat[1]
	pose.pose.orientation.z = quat[2]
	pose.pose.orientation.w = quat[3]
	return pose

def handle_interpolation_request(req):
	global act_position
	global act_orientation
	# sprawdzenie poprawnosci zadania
	int_time = req.time
	if int_time <= 0:
		return OINTRequestResponse("Invalid time")

	# przejscie na  czas dyskrenty
	samples = fps*int_time	
	if samples <= 0:
		return OINTRequestResponse("Invalid time")

	# cel interpolacji pozycji
	pose_goal = [0.0, 0.0, 0.0]
	pose_goal[0] = req.x
	pose_goal[1] = req.y
	pose_goal[2] = req.z
	
	#cel interpolacji orientacji
	orien_goal = [0.0, 0.0, 0.0]
	orien_goal[0] = req.roll
	orien_goal[1] = req.pitch
	orien_goal[2] = req.yaw

	r = rospy.Rate(fps)

	x_oint = JINT()
	y_oint = JINT()
	z_oint = JINT()
	roll_oint = JINT()
	pitch_oint = JINT()
	yaw_oint = JINT()

	k = 0

	while k <= samples:		
		# interpolacja polozenia
		x_pose = x_oint.interpole(req.interpolation_type, act_position[0], pose_goal[0], samples, k)
		y_pose = y_oint.interpole(req.interpolation_type, act_position[1], pose_goal[1], samples, k)
		z_pose = z_oint.interpole(req.interpolation_type, act_position[2], pose_goal[2], samples, k)

		# aktualizacja polozenia 
		act_position[0] = x_pose
		act_position[1] = y_pose
		act_position[2] = z_pose

		# interpolacja orientacji
		roll_pose = roll_oint.interpole(req.interpolation_type, act_orientation[0], orien_goal[0], samples, k)
		pitch_pose = pitch_oint.interpole(req.interpolation_type, act_orientation[1], orien_goal[1], samples, k)
		yaw_pose = yaw_oint.interpole(req.interpolation_type, act_orientation[2], orien_goal[2], samples, k)

		# aktualizacja orientacji
		act_orientation[0] = roll_pose
		act_orientation[1] = pitch_pose
		act_orientation[2] = yaw_pose
	
		# publikacja wyniku
		pose = create_pose()
		pub.publish(pose)
		k = k + 1
		r.sleep()
	return " Ready..."
	
def oint_server():
	global pub
	rospy.init_node('oint')
	s = rospy.Service('oint', OINTRequest, handle_interpolation_request)
	pub = rospy.Publisher('/pose_stamped', PoseStamped, queue_size = 30)	
	init_state = create_pose()
	rospy.sleep(0.3)
	pub.publish(init_state)
	rospy.spin()

if __name__ == "__main__":
	global act_position
	global act_orientation
	act_position = [0.0, 0.0, 0.0]
	act_orientation =  [0.0, 0.0, 0.0]
	oint_server()
