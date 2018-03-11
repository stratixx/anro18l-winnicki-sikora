#!/usr/bin/python
import rospy
while True:
	try:
		straight = str(raw_input("Podaj klawisz jazdy na wprost: "))
		if(len(straight)==1):
			break
		else:
			print("Nieprawidlowa dlugosc, podaj jeden klawisz")
	except ValueError:
		print("Nieprawidlowy klawisz")
while True:
	try:
		back = str(raw_input("Podaj klawisz jazdy do tylu: "))
		if(len(back)==1):
			break
		else:
			print("Nieprawidlowa dlugosc, podaj jeden klawisz")
	except ValueError:
		print("Nieprawidlowy klawisz: ")

while True:
	try:
		left = str(raw_input("Podaj klawisz skretu w lewo: "))
		if(len(left)==1):
			break
		else:
			print("Nieprawidlowa dlugosc, podaj jeden klawisz")
	except ValueError:
		print("Nieprawidlowy klawisz: ")

while True:
	try:
		right = str(raw_input("Podaj klawisz skretu w prawo: "))
		if(len(right)==1):
			break
		else:
			print("Nieprawidlowa dlugosc, podaj jeden klawisz")
	except ValueError:
		print("Nieprawidlowy klawisz: ")

try:
	rospy.set_param('straight', straight)
	rospy.set_param('back', back)
	rospy.set_param('left', left)
	rospy.set_param('right', right)
except Exception: 
	print("Wystapil blad. Sprawdz czy roscore jest uruchomiony")
else:
	print("Nowe ustawienie sterowania.")
	print('Wprost: {0}'.format(rospy.get_param('straight')))
	print('Tyl: {0}'.format(rospy.get_param('back')))
	print('Lewo: {0}'.format(rospy.get_param('left')))
	print('Prawo: {0}'.format(rospy.get_param('right')))
