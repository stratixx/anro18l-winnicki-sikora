#!/usr/bin/env python 

import sys
import math
try:
	if len(sys.argv) != 5:
		raise Exception

except Exception:
	print("Za malo argumentow")
	sys.exit()
a = float(sys.argv[1])
d = float(sys.argv[2])
alfa = float(sys.argv[3])
theta = float(sys.argv[4])

ct = math.cos(theta)
st = math.sin(theta)

ca = math.cos(alfa)
sa = math.sin(alfa)

r11 = ct
r12 = -st*ca
r13 = st*sa

r21 = st
r22 = ct*ca
r23 = -ct*sa

r31 = 0
r32 = sa
r33 = ca

rot_matrix = [[r11, r12, r13], [r21, r22, r23], [r31, r32, r33]]

rpy = [math.atan2(r21, r11), math.atan2(-r31, math.sqrt(r32 ** 2 + r33 ** 2)), math.atan2(r32, r33)]

print("roll = {0}".format(rpy[0]))
print("pitch = {0}".format(rpy[1]))
print("yaw = {0}".format(rpy[2]))


