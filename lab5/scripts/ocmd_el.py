#!/usr/bin/env python 
import rospy
from lab4.srv import *
import numpy as np
import math

rospy.wait_for_service('oint')
interpol_req = rospy.ServiceProxy('oint', OINTRequest)

t = np.linspace(0,6.28)
a = 0.220
b = 0.1
i = 0
while True:
	y = a*math.cos(t[i])
	z = b*math.sin(t[i]) + 0.4

	try:
		resp = interpol_req(float(0.433), 
				    float(y), 
				    float(z),
				    float(0), 
				    float(0), 
				    float(0),
			   	    float(0.1),
				    str('linear'))

	except rospy.ServiceException as exc:
		print("Service did not process request: " + str(exc))

	i = i + 1
	if i == 50:
		i = 0
