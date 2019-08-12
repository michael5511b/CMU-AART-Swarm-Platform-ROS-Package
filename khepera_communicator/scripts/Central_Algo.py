#!/usr/bin/env python

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
	pub = rospy.Publisher('K4_controls_150', K4_controls, queue_size=10)
	rospy.init_node('Central_Algo', anonymous=True)
	rate = rospy.Rate(100) # 10hz
	msg = K4_controls()
	while not rospy.is_shutdown():
		end = time.time()
		t = end - start
		msg.ctrl_W = 1
		msg.ctrl_V = 200 

		#rospy.loginfo(msg)
		pub.publish(msg)
		rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass