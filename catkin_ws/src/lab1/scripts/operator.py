#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3


straight = rospy.get_param("/straight")
back = rospy.get_param("/back")
left = rospy.get_param("/left")
right = rospy.get_param("/right")

def talker():
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('our_teleop', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        vel = Twist(Vector3(1.0, 0, 0), Vector3(0,0,0))	
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
