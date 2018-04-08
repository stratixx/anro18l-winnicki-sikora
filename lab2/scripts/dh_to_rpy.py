#!/usr/bin/env python 

#kolejnosc parametrow a, d, alfa, theta
import sys
import math
try:
	if len(sys.argv) != 5:
		raise Exception

except Exception:
	print("Za malo argumentow")
	sys.exit()

#parametry dh
a = float(sys.argv[1])
d = float(sys.argv[2])
alfa = float(sys.argv[3])
theta = float(sys.argv[4])

#obliczanie cosinusow i sinusow katow
ct = math.cos(theta)
st = math.sin(theta)

ca = math.cos(alfa)
sa = math.sin(alfa)

#parametry macierzy rotacji
r11 = ct
r12 = -st*ca
r13 = st*sa

r21 = st
r22 = ct*ca
r23 = -ct*sa

r31 = 0
r32 = sa
r33 = ca

#macierz rotacji
rot_matrix = [[r11, r12, r13], [r21, r22, r23], [r31, r32, r33]]

#katy rpy 
rpy = [math.atan2(r21, r11), math.atan2(-r31, math.sqrt(r32 ** 2 + r33 ** 2)), math.atan2(r32, r33)]

print("roll = {0}".format(rpy[0]))
print("pitch = {0}".format(rpy[1]))
print("yaw = {0}".format(rpy[2]))


