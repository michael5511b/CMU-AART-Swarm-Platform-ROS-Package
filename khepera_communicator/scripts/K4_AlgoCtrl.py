#!/usr/bin/env python

import socket
import sys
import time
import math
import numpy as  np
import matplotlib.pyplot as plt 
import rospy
from std_msgs.msg import String
#from khepera_communicator.msg import K4_controls, Acc, Gyro, Encoder_POS, Encoder_SPD, Time
from khepera_communicator.msg import K4_controls, SensorReadings

t = 0
started = False

rospy.init_node('K4_Algorithm_Controller', anonymous=True)


# Get all the sensor reading topic names for all the currently running K4_Comm nodes (all running Kheperas)
topic_list = rospy.get_published_topics() #[[topic1, type1]...[topicN, typeN]]

# We only want the name of the topics, 
topic_name_list = [] 
for i in range(len(topic_list)):
	topic_name_list.append(topic_list[i][0])

# Find the topics that contains the "Sensor_Readings_" title
sensor_topic_list = [s for s in topic_name_list if "Sensor_Readings_" in s]
sensor_topic_list = [x[1:] for x in sensor_topic_list] # There the topic names look like /Sensor_Readings_2000", we don't want the "/"
port_num_list = [x[-4:] for x in sensor_topic_list]
sensor_topic_cnt = len(sensor_topic_list)
print "Number of sensor reading topics: ", sensor_topic_cnt
print "All sensor readings topics: ", sensor_topic_list
#print port_num_list
"""
pub = []
for i in range(sensor_topic_cnt):
	pub.append(rospy.Publisher('K4_controls_' + str(port_num_list[i]), K4_controls, queue_size=10))
"""
p = rospy.Publisher('K4_controls_2000' , K4_controls, queue_size=10)

msg = K4_controls()
"""
def callback(data):
	rospy.loginfo(data)

	global t
	global started
	t = data.time
	
	if (not started):
		started = True
"""



def callback(data):
	print("callback")
	global p
	global t
	global msg
	t = data.time
	

	msg.ctrl_W = 0
	msg.ctrl_V = 200 * math.sin(t * 3.14159) 
	
	rospy.loginfo(msg)
	#pub[0].publish(msg)
	p.publish(msg)

def K4_AlgoCtrl():
	"""
	p = []
	for i in range(sensor_topic_cnt):
		p.append(rospy.Publisher('K4_controls_' + port_num_list[i], K4_controls, queue_size=10))
	"""
	# p = rospy.Publisher('K4_controls_2000' , K4_controls, queue_size=10)

	#msg = K4_controls()

	#msg.ctrl_W = 0
	#msg.ctrl_V = 200 * math.sin(t) 

	#rospy.init_node('K4_Algorithm_Controller', anonymous=True)
	#while not rospy.is_shutdown():
	#rospy.loginfo(msg)
	#pub.publish(msg)
	#m = K4_controls()
	#m.ctrl_V = 0
	#m.ctrl_W = 0
	#rospy.loginfo(m)
	#for i in range(sensor_topic_cnt):
	#	pub[i].publish(m)

	"""
	sub = []
	for i in range(sensor_topic_cnt):
		sub.append(rospy.Subscriber(sensor_topic_list[i], SensorReadings, callback))
	"""
	while not rospy.is_shutdown():
		p.publish(msg)
		print("1")
		rospy.Subscriber('Sensor_Readings_2000', SensorReadings, callback)
		print("2")
		rospy.spin()

if __name__ == '__main__':
	try:
		K4_AlgoCtrl()
	except rospy.ROSInterruptException:
		pass