#!/usr/bin/env python
# license removed for brevity

import rospy
import math
import time
import numpy as np
from std_msgs.msg import String

# Import message file
from khepera_communicator.msg import K4_controls, SensorReadings

start = time.time()

# These control commands are generated from OptimTraj, split into array

fileV = open("V.txt","r+") 
V = fileV.readlines()
fileW = open("W.txt","r+") 
W = fileW.readlines()


# Convert string array to float array
v = []
w = []
for i in range(len(V)):
	v.append(float(V[i]))
	w.append(float(W[i]))


def talker():
	i = 0
	# Set up publisher
	pub = rospy.Publisher('K4_controls_150', K4_controls, queue_size=10)
	rospy.init_node('Central_Algo', anonymous=True)
	
	# 1 min from start to finish, 6000 set of control commands, thus the refresh rate is 100 hz 
	rate = rospy.Rate(100) # 10hz
	
	# Message type
	msg = K4_controls()

	# Publish the control commands
	while not rospy.is_shutdown():
		if i < len(v):
			end = time.time()
			t = end - start
			msg.ctrl_W = w[i]
			msg.ctrl_V = v[i]
			i = i + 1

			rospy.loginfo(msg)
			pub.publish(msg)
			rate.sleep()
		else:
			end = time.time()
			t = end - start
			msg.ctrl_W = 0
			msg.ctrl_V = 0
			i = i + 1

			pub.publish(msg)
			rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass