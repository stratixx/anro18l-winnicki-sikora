#!/usr/bin/env python
import rospy

used_keys = []

while True:
	try:
		straight = str(raw_input("Podaj klawisz jazdy na wprost: "))
		if(len(straight)==1 and used_keys.count(straight) == 0):
			used_keys.append(straight)
			break
		elif(len(straight)!=1):
			print("Nieprawidlowa dlugosc, podaj jeden klawisz")
		else:
			print("Klawisz juz uzyty. Wybierz inny")

	except ValueError:
		print("Nieprawidlowy klawisz")
while True:
	try:
		back = str(raw_input("Podaj klawisz jazdy do tylu: "))
		if(len(back)==1 and used_keys.count(back) == 0):
			used_keys.append(back)
			break
		elif(len(back)!=1):
			print("Nieprawidlowa dlugosc, podaj jeden klawisz")
		else:
			print("Klawisz juz uzyty. Wybierz inny")

	except ValueError:
		print("Nieprawidlowy klawisz: ")

while True:
	try:
		left = str(raw_input("Podaj klawisz skretu w lewo: "))
		if(len(left)==1 and used_keys.count(left) == 0):
			used_keys.append(left)
			break
		elif(len(left)!=1):
			print("Nieprawidlowa dlugosc, podaj jeden klawisz")
		else:
			print("Klawisz juz uzyty. Wybierz inny")

	except ValueError:
		print("Nieprawidlowy klawisz: ")

while True:
	try:
		right = str(raw_input("Podaj klawisz skretu w prawo: "))
		if(len(right)==1 and used_keys.count(right) == 0):
			used_keys.append(right)
			break
		
		elif(len(right)!=1):
			print("Nieprawidlowa dlugosc, podaj jeden klawisz")
		else:
			print("Klawisz juz uzyty. Wybierz inny")
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
