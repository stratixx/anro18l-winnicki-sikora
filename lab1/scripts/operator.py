import rospy
import sys
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
# Pobranie parametrow z ewentualnym ustawieniem wartosci domyslnych
def init_params():
	if rospy.has_param('straight'):
		straight = rospy.get('straight')
	else:
		straight = 'w'

	if rospy.has_param('back'):
		back = rospy.get('back')
	else:
		back = 's'

	if rospy.has_param('left'):
		left = rospy.get('left')
	else:
		left = 'a'

	if rospy.has_param('right'):
		right = rospy.get('right')
	else:
		right = 'd'

def getkey(prompt=""):
    import termios, sys, tty
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ECHO          # lflags
    try:
		termios.tcsetattr(fd, termios.TCSADRAIN, new)
		tty.setraw(sys.stdin.fileno())
		key = sys.stdin.read(1)
		if(key == '\x1a'):
			sys.exit(0)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return key


def talker():
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('our_teleop', anonymous=True)
    rate = rospy.Rate(10) 
    while not rospy.is_shutdown():
		if (getkey() == straight):
        	vel = Twist(Vector3(2.0, 0, 0), Vector3(0.0,0,0))	
        	pub.publish(vel)

		if (getkey() == back):
        	vel = Twist(Vector3(-2.0, 0, 0), Vector3(0.0,0,0))	
        	pub.publish(vel)

		if (getkey() == left):
        	vel = Twist(Vector3(0.0, 0, 0), Vector3(0.0,0,2.0))	
        	pub.publish(vel)

		if (getkey() == right):
        	vel = Twist(Vector3(0.0, 0, 0), Vector3(0.0,0,2.0))	
        	pub.publish(vel)

        rate.sleep()

init_params()

print ('Reading from keyboard')
print ('---------------------------')
print ('Przod: ', straight, ', Tyl: ', back,', Lewo: ', left,', Prawo: ', right)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
