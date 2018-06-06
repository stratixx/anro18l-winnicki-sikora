#!/usr/bin/env python


import numpy as np
from scipy import optimize
import rospy
from math import *

from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
import robot

pi = np.pi	
th3 = 0
fps = 60#rospy.get_param('fps')
a2 = rospy.get_param('a2')
a3 = rospy.get_param('gripper')
bh = 0.3
z = 0.3

class NoSolutionException(Exception):
	def __init__(self):
		super(Exception)

class Result:
	def __init__(self, t1, t2 ,t3):
		self.t1 = t1
		self.t2 = t2
		self.t3 = t3

last_res = Result(0, 0, 0)

def fun_z(th2):
	global th3
	return z - bh + a2*sin(th2) + a3*sin(th2 + th3)

def ROTZ(theta):
	A = np.array([[np.cos(theta), -np.sin(theta), 0, 0], [np.sin(theta), np.cos(theta), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
	return A

def TRANSX(a):
	A = np.array([[1, 0, 0, a], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
	return A

def ROTX(alpha):
	A = np.array([[1, 0, 0, 0], [0, np.cos(alpha), -np.sin(alpha), 0], [0, np.sin(alpha), np.cos(alpha), 0], [0, 0, 0, 1]])
	return A

def TRANSZ(d):
	A = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, d], [0, 0, 0, 1]])
	return A

def th1_cos(x, t2, t3):
	den = (a2*cos(t2) + a3*cos(t2 + t3))
	#den = (a2*cos(t2) + a3*sin(t3))
	"""
	if den > 1:
		den = den - 1
	if den < -1:
		den = den + 1
	"""
	return acos(x/den)

def th1_sin(y, t2, t3):
	den = (a2*cos(t2) + a3*cos(t2 + t3))
	#den = (a2*cos(t2) + a3*sin(t3))
	"""
	if den > 1:
		den = den - 1
	if den < -1:
		den = den + 1
	"""
	return asin(y/den)


def find_all_t2_and_t3(z):
	i = 0
	global th3
	pairs = []
	t3_d = np.linspace(0, np.pi/2, num=100)
	sol = np.zeros(100)
	#print('finding t2 t3')
	while i < 100:
		th3 = t3_d[i]
		tmp = optimize.root(fun_z, 0)
		sol[i] = tmp.x
		result = [sol[i], th3]
		pairs.append(result)
		i = i + 1
		#print(result)
	return pairs

def find_t1(pairs, x, y):
	angles = []
	#print('finding t1 -------------------------------------------')
	for pair in pairs:
		try:
			t1c = th1_cos(x, pair[0], pair[1])
			#print(result1)
		except ValueError:
			pass

		try:
			t1s = th1_cos(x, pair[0], pair[1])
			
			#print(result2)
		except ValueError:
			pass


		if t1c - t1s > 0.1:
			continue

		t1 = (t1c + t1s)/2
	
		result = [t1, pair[0], pair[1]]
		angles.append(result)	
		
	return angles

def check_angle_values(angles):
	proper_angles = []
	#print('poprawnie wartosci')
	for ang in angles:
		try:
			"""if ang[0] > pi or ang[0] < -pi:
				rospy.logerr("Zly kat")
				raise Exception"""
	
			if ang[1] > 0 or ang[1] < -pi/2:
				rospy.logerr("Zly kat")
				raise Exception
	
			if ang[2] < 0 or ang[2] > pi/2:
				rospy.logerr("Zly kat")
				raise Exception	
		except Exception:
			continue
		#print(ang)
		proper_angles.append(ang)
	return proper_angles

def check_solution(ang, xz, yz, zz):
	results = []
	robot = []

	staw1 = [0, 0, 0, 0]
	staw2 = [0, 0, -pi/2, 0]
	staw3 = [a2, 0, 0, 0]
	staw4 = [a3, 0, 0, 0]

	robot.append(staw1)
	robot.append(staw2)
	robot.append(staw3)
	robot.append(staw4)

	robot[0][3] = ang[0]
	robot[1][3] = ang[1]
	robot[2][3] = ang[2]

	joints = []
	
	# obliczenie macierzy zlacz
	for staw in robot:
		R1 = ROTX(staw[2])
		R2 = TRANSX(staw[0])
		R3 = ROTZ(staw[3])
		R4 = TRANSZ(staw[1])
		R = np.dot(R1,R2)
		R = np.dot(R, R3)
		R = np.dot(R, R4)
		joints.append(R)
	
	# obliczenie kinematyki prostej
	KIN0_1 = np.dot(joints[0],joints[1])
	KIN1_2 = np.dot(KIN0_1, joints[2])
	KIN2_3 = np.dot(KIN1_2, joints[3])
	KIN = KIN2_3

	# obliczenie pozycji koncowki	
	pos_zero = np.array([0, 0, 0, 1]).transpose()
	pos = np.dot(KIN, pos_zero)
	
	err = sqrt((pos[0] -xz)**2 + (pos[1] - yz)**2 + (pos[2] - zz)**2)		
	results = [ang[0], ang[1], ang[2], err]

	return results
			 

def minimize_change(angs):
	index_best = 0
	act_ind = 0
	act_min_error = 1000
	for res in angs:
		if res[3] < act_min_error:
			act_min_error = res[3]
			index_best = act_ind
		act_ind = act_ind + 1
	#print('NAJMNIEJSZY BLAD DLA ----------------------------------------')
	#print(act_min_error)
	best_res = angs[index_best]
	return Result(best_res[0], best_res[1], best_res[2])
			
		

def callback(data):
	global last_res
	ointPose = data
	x = ointPose.pose.position.x
	y = ointPose.pose.position.y
	z = ointPose.pose.position.z
	a2 = rospy.get_param('a2')
	a3 = rospy.get_param('gripper')
	"""
	try:
		print("-----------------------------------")
		# mozliwe rozwiazania rownania
		ts = find_all_t2_and_t3(z)
		print("znalezionych par t2 i t3: {0}".format(len(ts)))
		if len(ts) == 0:
			raise NoSolutionException

		# mozliwe zestawy rozwiazan
		angs = find_t1(ts, x, y)
		print("znalezionych konfiguracji: {0}".format(len(angs)))
		if len(angs) == 0:
			raise NoSolutionException

		# sprawdzenie dziedziny
		p_angs = check_angle_values(angs)
		print("znalezionych rozwiazan w dziedzinie: {0}".format(len(p_angs)))
		if len(p_angs) == 0:
			raise NoSolutionException		
	
		# sprawdzenie poprawnosci rozwiazan
		
		results = check_solution(p_angs, x, y, z)
		print("znalezionych poprawnych  konfiguracji: {0}".format(len(results)))
		if len(results) == 0:
			raise NoSolutionException		
	

		# wybor najlepszego rozwiazania
		best = minimize_change(results)
		print("najlepsza konfiguracja: t1 = {0}, t2= {1}, t3 = {2}".format(best.t1, best.t2, best.t3))

		#ustaw katy
		robot.set_angles(best.t1, best.t2, best.t3)
		last_res = best
		state = robot.get_joint_state(fps)	
		pub.publish(state)	
	
	except NoSolutionException:
		print('No solution')
		rospy.logerr("No solution")
	"""
	
	try:
		zz = z - bh
		t1 = atan2(y,x)
		h = pow((x/cos(t1)),2) + pow(zz,2)
		t2 = -atan2(zz*cos(t1),x) - acos((pow(a2,2) - pow(a3,2)+h)/(2*a2*pow(h,0.5)))
		t3 = acos((-pow(a2,2) - pow(a3,2) + h)/(2*a2*a3))	
		results = check_solution([t1, t2, t3], x, y, z)
		print(results[3])	
	except Exception:
		return

	robot.set_angles(t1, t2, t3)
	state = robot.get_joint_state(fps)	
	pub.publish(state)

def listener():
	# init node
	rospy.init_node('IKIN', anonymous=False)
	rospy.Subscriber('/pose_stamped', PoseStamped, callback)
	global pub 	
	pub = rospy.Publisher('/joint_states', JointState, queue_size = 30)
	robot.set_angles(0, 0, 0)
	state = robot.get_joint_state(fps)	
	pub.publish(state)

	rospy.spin()	
	
if __name__ == '__main__':
	robot = robot.Robot()
	listener()
