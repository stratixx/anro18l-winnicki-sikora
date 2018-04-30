#!/usr/bin/env python 

#params joint0, joint1, joint2, time, interpolation_type
import sys
from std_msgs.msg import String
try:
	if len(sys.argv) != 5:
		raise Exception

except Exception:
	print("Za malo argumentow")
	sys.exit()

import rospy
from lab4.srv import *


rospy.wait_for_service('jint')
interpol_req = rospy.ServiceProxy('jint', InterpolationRequest)


try:
	resp = interpol_req(float(sys.argv[1]), 
			    float(sys.argv[2]), 
			    float(sys.argv[3]),
		   	    float(sys.argv[4]),
			   'quad_spline')
except rospy.ServiceException as exc:
	print("Service did not process request: " + str(exc))

print(resp)
