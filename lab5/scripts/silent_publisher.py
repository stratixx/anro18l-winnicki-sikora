#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState

def talker():
	rospy.init_node('silent_publisher', anonymous="True")
	rate = rospy.Rate(30)
	msg = JointState()
	msg.name = []
	msg.position = []
	msg.velocity = []
	msg.effort = []
	msg.name.append('base_link_to_segment_1_joint_continuous')
	msg.position.append(0.00)
	msg.name.append('segment_1_to_segment_2_joint_continuous')
	msg.position.append(0.00)
	msg.name.append('segment_2_to_gripper_joint_continuous')
	msg.position.append(0.00)
	msg.header.stamp = rospy.Time.now()
	msg.header.frame_id = 'base_link'

	pub = rospy.Publisher('joint_states', JointState, queue_size=10)
	counter = 0
    	while counter < 30:
		pub.publish(msg)
		rate.sleep()
		counter = counter + 1
	rospy.signal_shutdown('Quit')



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
