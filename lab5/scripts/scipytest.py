#!/usr/bin/env python


import numpy as np
from math import *
from scipy import optimize

th3 = 0

class Result:
	def __init__(self, t1, t2 ,t3):
		self.t1 = t1
		self.t2 = t2
		self.t3 = t3

def fun_z(th2):
	return z - bh + a2*sin(th2) + a3*sin(th2 + th3)

def th1_cos(x, t2, t3):
	return acos(x/(a2*cos(t2) + a3*cos(t2 + t3)))

def th1_sin(y, t2, t3):
	return asin(y/(a2*cos(t2) + a3*cos(t2 + t3)))
	
x = 0.2999
y = 0.2750
z = 0.3992
a2 = 0.4
a3 = 0.1
bh = 0.3

t3_d = np.linspace(0, np.pi/2, num=100)
sol = np.zeros(100)

results = []

i = 0
while i < 100:
	th3 = t3_d[i]
	tmp = optimize.root(fun_z, 0)
	sol[i] = tmp.x
	
	try:
		t1c= th1_cos(x, sol[i], t3_d[i])
		t1s= th1_sin(y, sol[i], t3_d[i])	
		if(t1c - t1s > 0.001):
			i = i + 1
			continue
	except ValueError:
		t1c = 1000
		t1s = 1000
		i = i + 1
		continue

	res = Result(t1c, sol[i], t3_d[i])
	results.append(res)
	print('---------')
	print(t1c)
	print(sol[i])
	print(t3_d[i])
	i = i + 1




