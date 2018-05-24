#!/usr/bin/env python 

#params x, y, z, roll, pitch, yaw time, interpolation_type
import sys
from std_msgs.msg import String
try:
	if len(sys.argv) != 9:
		raise Exception

except Exception:
	print("Za malo argumentow")
	sys.exit()

import rospy
from lab4.srv import *

rospy.wait_for_service('oint')
interpol_req = rospy.ServiceProxy('oint', OINTRequest)


try:
	resp = interpol_req(float(sys.argv[1]), 
			    float(sys.argv[2]), 
			    float(sys.argv[3]),
			    float(sys.argv[4]), 
			    float(sys.argv[5]), 
			    float(sys.argv[6]),
		   	    float(sys.argv[7]),
			    str(sys.argv[8]))

except rospy.ServiceException as exc:
	print("Service did not process request: " + str(exc))

print(resp)
