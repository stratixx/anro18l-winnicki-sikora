#!/usr/bin/env python

import rospy
#import sys
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

# Pobranie parametrow z ewentualnym ustawieniem wartosci domyslnych
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

def talker():
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('our_teleop', anonymous=True)
    rate = rospy.Rate(10) 
    while not rospy.is_shutdown():
	#if sys.stdin.read(1):
        	vel = Twist(Vector3(1.0, 0, 0), Vector3(1.0,0,0))	
        	pub.publish(vel)
        rate.sleep()


print 'Reading from keyboard'
print '---------------------------'
print 'Przod: ', straight, ', Tyl: ', back,', Lewo: ', left,', Prawo: ', right

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
