#!/usr/bin/env python


import numpy as np
import rospy
import math

from geometry_msgs.msg import PoseStamped
from tf.transformations import quaternion_from_euler
from lab4.srv import *

pi = np.pi

global fps
fps = rospy.get_param('fps')

global pub # publisher


def handle_interpolation_request(req):
	# sprawdzenie poprawnosci zadania
	int_time = req.time
	if int_time <= 0:
		return JINTRequestResponse("Invalid time")

	# przejscie na  czas dyskrenty
	samples = fps*int_time	
	if samples <= 0:
		return JINTRequestResponse("Invalid time")

	# cel interpolacji


def oint_server()
	rospy.init_node('oint')
	s = rospy.Service('oint', JINTRequest, handle_interpolation_request)
	pub = rospy.Publisher('/pose_stamped', PoseStamped, queue_size = 10)	
	init_state = PoseStamped()
	init_state
	rospy.sleep(0.3)
	pub.publish(init_state)
	rospy.spin()

if __name__ == "__main__":
	oint_server()
