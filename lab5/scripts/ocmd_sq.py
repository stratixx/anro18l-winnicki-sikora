#!/usr/bin/env python 
import rospy
from lab4.srv import *


rospy.wait_for_service('oint')
interpol_req = rospy.ServiceProxy('oint', OINTRequest)
table = [[0.433, 0.1, 0.3], [0.433, 0.1, 0.500], [0.433, -0.1, 0.500], [0.433, -0.1, 0.3]]
i = 0
while True:

	try:
		resp = interpol_req(float(table[i][0]), 
				    float(table[i][1]), 
				    float(table[i][2]),
				    float(0), 
				    float(0), 
				    float(0),
			   	    float(1),
				    str('linear'))

	except rospy.ServiceException as exc:
		print("Service did not process request: " + str(exc))

	i = i + 1
	if i == 4:
		i = 0

