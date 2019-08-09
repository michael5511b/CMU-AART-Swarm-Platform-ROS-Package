#!/usr/bin/env python

import socket
import sys
import time
import math
import numpy as  np
import matplotlib.pyplot as plt 

# Imports from ROS
import rospy
from std_msgs.msg import String

# Import message file
from khepera_communicator.msg import K4_controls, SensorReadings

# Server socket port input at script launch
print "========== Khepera IV Communicatoion Driver Node =========="
var = raw_input("Please enter the port number: ")
print "you entered", var
UDP_PORT_NO = int(var) #UDP Port number of this Khepera robot


# creating socket (DGRAM is data gram, how UDP works)
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind(('192.168.1.142', UDP_PORT_NO))
#serverSock.bind(('192.168.0.101', UDP_PORT_NO))



# Establish the node 
# (the name of the node will end with the port number, ex: 'K4_Comm_3000' for port 3000)
rospy.init_node('K4_Communicator_' + str(UDP_PORT_NO), anonymous=True)


# Establish the publisher and topic
# (publish to a sensor reading topic, the name will end with the port number, ex: 'sensor_readgins_3000' for port 3000)
pub = rospy.Publisher('Sensor_Readings_' + str(UDP_PORT_NO), SensorReadings, queue_size=10)


# Initialize angular(W) and linear(V) velocity control variables
W = 0
V = 0

# Initialize global variable for Khepera address
# addr = ('',1)
Trig = False
msg = SensorReadings()
# print("1")
def callback(Sub_data):
	# Publishing and getting subscribed data are in the same callback function
	# to maintain a "get one set of data, end one set of data" sequence

	# msg type
	global msg
	global Trig
	global Time_val_khepera
	global khepera_freq
	global t_old_khepera 
	global data
	global addr
	# global serverSock
	print("1")
	
	

	# recieve sensor data form khepera
	if Trig == False:
		Trig = True
		print("2")
	else:
		serverSock.settimeout(1)

	data, addr = serverSock.recvfrom(1024)
	# set a timeout for the socket or the UDP connection will stall once a packet is lost (which happens very often)
	

	# recieve sensor information in a string stored in the variable 'data'
	# 'addr' records the address of the Khepera where the sensor reading string is sent from
	#data, addr = serverSock.recvfrom(1024)


	# Decoding the sensor data string sent from the Khepera
	# Khepera Time 
	T = data.split('T')[1] 
	# Accelerometer
	AX = data.split('AX')[1]
	AY = data.split('AY')[1]
	AZ = data.split('AZ')[1]
	# Gyroscope
	GX = data.split('GX')[1]
	GY = data.split('GY')[1]
	GZ = data.split('GZ')[1]
	# Encoder Position
	PL = data.split('PL')[1]
	PR = data.split('PR')[1]
	# Encoder Speed
	SL = data.split('SL')[1]
	SR = data.split('SR')[1]


	# Store the sensor data in ROS message corresponding to the type
	msg.time = float(T)
	msg.acc_x = float(AX)
	msg.acc_y = float(AY)
	msg.acc_z = float(AZ)
	msg.gyro_x = float(GX)
	msg.gyro_y = float(GY)
	msg.gyro_z = float(GZ)
	msg.pos_L = int(PL)
	msg.pos_R = int(PR)
	msg.spd_L = int(SL)
	msg.spd_R = int(SR)


	# Log and publish the message containing sensor data
	rospy.loginfo(msg)    		
   	pub.publish(msg)
	
	# Log angular and linear velocity controls
	rospy.loginfo(Sub_data)

	# Store angular and linear velocity controls in declared global variables
	global W 
	W = Sub_data.ctrl_W
	global V 
	V = Sub_data.ctrl_V

	# Send controls to the Khepera
	serverSock.sendto(str(W) + 'x' + str(V), addr)


def K4_Comm():
	# Will automatically subscribed to a K4 control topic with it's port number
	# ex: 'K4_controls_3000' for port 3000
	print("K4Comm")
	global s
	pub.publish(msg)
	s = rospy.Subscriber('K4_controls_' + var, K4_controls, callback)
	
	# spin function will loop the callback function, which contains the publishing and aquiring data from subscriber actions
	rospy.spin()

	


if __name__ == '__main__':
	try:
		K4_Comm()
	except rospy.ROSInterruptException:
		pass

# If interrupted by ctrl-c or stopped
# Stop the khepera and close the socket
#serverSock.sendto('0x0', addr)
#serverSock.close()

