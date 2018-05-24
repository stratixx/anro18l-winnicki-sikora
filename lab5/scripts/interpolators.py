import numpy as np 

class JINT:

	def __init__(self):
		self.last_t = 1000
		self.last_params = np.matrix('0; 0; 0; 0; 0; 0')

	### interpolacja liniowa ###
	def linear_interpolation(self,x0, x1, t1, t):
		a = (x1 - x0)/(t1)	
		return x0 + a*t 

	### interpolacja splajnowa z dwoma funkcjami kwadratowymi ###
	def quad_spline_interpolation(self,x0, x1, t1, t):
		if self.last_t == (t - 1):
			params = self.last_params
		else:
			spline_array = np.array([[0, 0, 1, 0, 0, 0], 
						  [0, 0, 0, t1**2, t1, 1], 
						  [0, 1, 0, 0, 0, 0], 
						  [0, 0, 0, 2*t1, 1, 0], 
						  [(t1/2)**2, (t1/2), 1, -((t1/2)**2), -(t1/2), -1], 
						  [t1, 1, 0, -t1, -1, 0]])
			b = np.array([[x0],[x1],[0],[0],[0],[0]])
			params = np.linalg.solve(spline_array, b)
			params = params.tolist()
			self.last_params = params
		
		self.last_t = t
		#print(params)
		if t < (t1/2):
			return params[0][0]*(t**2) + params[1][0]*t + params[2][0]
		else:
			return params[3][0]*(t**2) + params[4][0]*t + params[5][0]

	### interpolacja z trapezowym przebiegiem predkosci ###
	def trapezoid_vel_interpolation(self, x0, x1, t1, t):
		if self.last_t == (t - 1):
			params = self.last_params
		else:
			spline_array = np.array([[0, 0, 1, 0, 0, 0, 0, 0],
						  [0, 0, 0, 0, 0, t1**2, t1, 1],
						  [(t1**2)/25, t1/5, 1, -t1/5, -1, 0, 0, 0],
						  [0, 0, 0, 4*t1/5, 1, -(4*t1/5)**2, -4*(t1/5), -1],
						  [2*t1/5, 1, 0, -1, 0, 0, 0, 0],
						  [0, 0, 0, 1, 0, -8*t1/5, -1, 0],
						  [0, 1, 0, 0, 0, 0, 0, 0],
						  [0, 0, 0, 0, 0, 2*t1, 1, 0]])
			b = np.array([[x0],[x1],[0],[0],[0],[0],[0],[0]])
			params = np.linalg.solve(spline_array, b)
			params = params.tolist()
			self.last_params = params
			
		self.last_t = t
		#print(params)
		if t < (t1/5):
			return params[0][0]*(t**2) + params[1][0]*t + params[2][0]
		if t >= t1/5 and t < (4*t1/5):
			return params[3][0]*t + params[4][0]
		else:
			return params[5][0]*(t**2) + params[6][0]*t + params[7][0]
		
	### wybranie odpowiedniego trybu interpolacji ###
	def interpole(self, type, x0, x1, t1, t):
		if type == 'linear':
			return self.linear_interpolation(x0, x1, t1, t)
		if type == 'quad_spline':
			return self.quad_spline_interpolation(x0, x1, t1, t)
		if type == 'trapezoid_vel':
			return self.trapezoid_vel_interpolation(x0, x1, t1, t)

