#obiekt robota
import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped
import math
from tf.transformations import quaternion_from_euler

class Robot:
	def __init__(self):
		self.get_params()
		
		staw1 = [self.a0, self.d1, self.al0, 0]
		staw2 = [self.a1, self.d2, self.al1, 0]
		staw3 = [self.a2, self.d3, self.al2, 0]
		staw4 = [self.gripper, 0, 0, 0]
		
		self.joints = []
		self.joints.append(staw1)
		self.joints.append(staw2)
		self.joints.append(staw3)
		self.joints.append(staw4)

		self.joint_position = [0.0, 0.0, 0.0]

	def get_params(self):
		#wysokosc bazy
		self.base_height=rospy.get_param('base_height')
		self.gripper=rospy.get_param('gripper')

		# parametry robota
		self.a0 = rospy.get_param('a0')
		self.a1 = rospy.get_param('a1')
		self.a2 = rospy.get_param('a2') 
		self.d1 = rospy.get_param('d1') + self.base_height
		self.d2 = rospy.get_param('d2') 
		self.d3 = rospy.get_param('d3') 
		self.al0 = rospy.get_param('al0')
		self.al1 = rospy.get_param('al1')
		self.al2 = rospy.get_param('al2')


	def ROTZ(self,theta):
		A = np.array([[np.cos(theta), -np.sin(theta), 0, 0], [np.sin(theta), np.cos(theta), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
		return A

	def TRANSX(self,a):
		A = np.array([[1, 0, 0, a], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
		return A

	def ROTX(self,alpha):
		A = np.array([[1, 0, 0, 0], [0, np.cos(alpha), -np.sin(alpha), 0], [0, np.sin(alpha), np.cos(alpha), 0], [0, 0, 0, 1]])
		return A

	def TRANSZ(self,d):
		A = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, d], [0, 0, 0, 1]])
		return A

	def createPose(self, ang0, ang1, ang2):
		#sprawdzenie poprawnosci katow
		if ang0 > 3.14 or ang0 < -3.14:
			rospy.logerr("Zly kat")
			return
	
		if ang1 > 0 or ang1 < -1.54:
			rospy.logerr("Zly kat")
			return
	
		if ang2 < 0 or ang2 > 1.54:
			rospy.logerr("Zly kat")
			return

		#tablica macierzy
		matrices = []
	
		# obliczenie macierzy zlacz
		for staw in self.joints:
			R1 = self.ROTX(staw[2])
			R2 = self.TRANSX(staw[0])
			R3 = self.ROTZ(staw[3])
			R4 = self.TRANSZ(staw[1])
			R = np.dot(R1,R2)
			R = np.dot(R, R3)
			R = np.dot(R, R4)
			matrices.append(R)
	
		# obliczenie kinematyki prostej
		KIN0_1 = np.dot(matrices[0],matrices[1])
		KIN1_2 = np.dot(KIN0_1, matrices[2])
		KIN2_3 = np.dot(KIN1_2, matrices[3])
		KIN = KIN2_3
	
		# obliczenie pozycji koncowki	
		pos_zero = np.array([0, 0, 0, 1]).transpose()
		pos = np.dot(KIN, pos_zero)
	
		#generacja pozycji
		pose = PoseStamped()
		pose.header.stamp = rospy.Time.now()
		pose.header.frame_id = "base_link"

		# przesuniecie poczatku wektora nad baze	
		pose.pose.position.x = np.take(KIN, [3])
		pose.pose.position.y = np.take(KIN, [7])
		pose.pose.position.z = np.take(KIN, [11])
	
		#obliczenie katow rpy
		r11 = np.take(KIN, [0])
		r21 = np.take(KIN, [4])
		r31 = np.take(KIN, [8])
		r32 = np.take(KIN, [9])
		r33 = np.take(KIN, [10])
					
		r = math.atan2(r32, r33)
		p = math.atan2(-r31, math.sqrt(r32 ** 2 + r33 ** 2))
		y = math.atan2(r21, r11)
	
		# obliczenie kwaternionu
		quat = quaternion_from_euler(r, p, y)
		pose.pose.orientation.x = quat[0]
		pose.pose.orientation.y = quat[1]
		pose.pose.orientation.z = quat[2]
		pose.pose.orientation.w = quat[3]
	
		return pose

