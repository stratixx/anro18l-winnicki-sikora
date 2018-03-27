#!/usr/bin/env python
import rospy
import sys
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

# Nieblokujące pobranie wciśniętego klawisza, bez śladu w konsoli
def getkey(prompt=""):
    import termios, sys, tty
    fd = sys.stdin.fileno() 
    old = termios.tcgetattr(fd) # zapamiętaj poprzednie ustawienie terminala
    new = termios.tcgetattr(fd) # nowe ustawienie terminala
    new[3] = new[3] & ~termios.ECHO          
    try: # pobierz klawisz
		termios.tcsetattr(fd, termios.TCSADRAIN, new)
		tty.setraw(sys.stdin.fileno())
		key = sys.stdin.read(1)
		if(key == '\x1a'):
			sys.exit(0)	
    finally:
        	termios.tcsetattr(fd, termios.TCSADRAIN, old) # przywróc poprzednie ustawienia po pobraniu klawisza
    return key

# Procedura publishera
def talker():
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('our_teleop', anonymous=True)
    rate = rospy.Rate(100) 
    while not rospy.is_shutdown(): # na podstawie klawisza, wygeneruj odpowiednie sterowanie
		key = getkey()
		if (key == straight): # prosto
        		vel = Twist(Vector3(2.0, 0, 0), Vector3(0.0,0,0))	
        		pub.publish(vel)

		if (key == back): # tył
        		vel = Twist(Vector3(-2.0, 0, 0), Vector3(0.0,0,0))	
       			pub.publish(vel)

		if (key == left): # lewo
       			vel = Twist(Vector3(0.0, 0, 0), Vector3(0.0,0,2.0))	
       			pub.publish(vel)

		if (key == right): # prawo
       			vel = Twist(Vector3(0.0, 0, 0), Vector3(0.0,0,-2.0))	
       			pub.publish(vel)

       		rate.sleep() # zachowaj odpowiednią częstotliwość nadawania

# Procedura main, wczytanie klawuszy sterujących z serwera parametrów
# Jeśli serwer nie zawiera parametrów, ustawia domyślne 
if __name__ == '__main__':
	#init params
	if rospy.has_param('straight'):
		straight = rospy.get_param('straight')
	else:
		straight = 'w'

	if rospy.has_param('back'):
		back = rospy.get_param('back')
	else:
		back = 's'

	if rospy.has_param('left'):
		left = rospy.get_param('left')
	else:
		left = 'a'

	if rospy.has_param('right'):
		right = rospy.get_param('right')
	else:
		right = 'd'


	# czytaj sterowanie z klawiatury
	print('Reading from keyboard')
	print('---------------------')
	print('Przod: {0}, Tyl: {1}, Lewo: {2}, Prawo: {3}'.format(straight,back,left,right))
    	
	try:
       		talker()
    	except rospy.ROSInterruptException:
        	pass
