#!/usr/bin/env python
# license removed for brevity

import rospy
import math
import time
from std_msgs.msg import String
# Import message file
from khepera_communicator.msg import K4_controls, SensorReadings

start = time.time()

def talker():
	# Set up publisher
	pub = rospy.Publisher('K4_controls_154', K4_controls, queue_size=10)
	rospy.init_node('Central_Algo', anonymous=True)
	
	# Set publish rate
	# rate = rospy.Rate(100) # 10hz
	
	# Message type
	msg = K4_controls()

	while not rospy.is_shutdown():
		
		end = time.time()
		t = end - start
		
		msg.ctrl_W = 0
		msg.ctrl_V = 200 * math.sin(3.14159 * t) 

		#rospy.loginfo(msg)
		pub.publish(msg)
		#rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass