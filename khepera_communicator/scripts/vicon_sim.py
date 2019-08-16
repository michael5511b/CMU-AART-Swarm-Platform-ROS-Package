#!/usr/bin/env python

import rospy
import math
import time
from std_msgs.msg import String
# Import message file
from khepera_communicator.msg import K4_controls, SensorReadings
from geometry_msgs.msg import TransformStamped

# For time recording 
start = time.time()

def sim():
	p1 = rospy.Publisher('vicon/k150/k150', TransformStamped, queue_size=10)
	p2 = rospy.Publisher('vicon/k154/k154', TransformStamped, queue_size=10)
	p3 = rospy.Publisher('vicon/k158/k158', TransformStamped, queue_size=10)
	rospy.init_node('vicon_sim', anonymous=True)
	
	msg1 = TransformStamped()
	
	msg2 = TransformStamped()
	
	msg3 = TransformStamped()
	

	rate = rospy.Rate(100) # 10hz

	while not rospy.is_shutdown():

		end = time.time()
		t = end - start
		
		msg1.transform.translation.x = 1 * math.sin(t)
		msg1.transform.translation.y = 1 * math.sin(3.1415 * t)
		msg2.transform.translation.x = 2 * math.sin(t)
		msg3.transform.translation.x = 3 * math.sin(t)

		rospy.loginfo(msg1)
		rospy.loginfo(msg2)
		rospy.loginfo(msg3)

		p1.publish(msg1)
		p2.publish(msg2)
		p3.publish(msg3)

		rate.sleep()

if __name__ == '__main__':
	try:
		sim()
	except rospy.ROSInterruptException:
		pass