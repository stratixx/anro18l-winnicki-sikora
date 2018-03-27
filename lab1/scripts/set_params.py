#!/usr/bin/env python
import rospy

# klasa settera klawiszy sterujących
class param_setter:
	def __init__(self):
		self.used_keys = []
		self.inputs = {'straight': "Podaj klawisz jazdy na wprost: ", 'back' : "Podaj klawisz jazdy do tylu: ", 'left' : "Podaj klawisz skretu w lewo: ", 'right' : "Podaj klawisz skretu w prawo: "}

	def get_param(self, param):
		while True:
			try:
				key = str(raw_input(self.inputs[param]))
				if(len(key)==1 and self.used_keys.count(key) == 0):
					self.used_keys.append(key)
					break
				elif(len(key)!=1):
					print("Nieprawidlowa dlugosc, podaj jeden klawisz")
				else:
					print("Klawisz juz uzyty. Wybierz inny")
		
			except ValueError:
				print("Nieprawidlowy klawisz")
		return key

setter = param_setter()

# zapisanie nowych klawiszy sterujących do serwera parametrów
try:
	rospy.set_param('straight', setter.get_param('straight'))
	rospy.set_param('back', setter.get_param('back'))
	rospy.set_param('left', setter.get_param('left'))
	rospy.set_param('right', setter.get_param('right'))
	
except Exception: 
	print("Wystapil blad. Sprawdz czy roscore jest uruchomiony")
else:
	print("Nowe ustawienie sterowania.")
	print('Wprost: {0}'.format(rospy.get_param('straight')))
	print('Tyl: {0}'.format(rospy.get_param('back')))
	print('Lewo: {0}'.format(rospy.get_param('left')))
	print('Prawo: {0}'.format(rospy.get_param('right')))
