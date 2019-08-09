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
var = raw_input("Please enter the last three digit of the khepera's IP: ")
print "you entered: ", var
IP_NO = int(var) #UDP Port number of this Khepera robot


# creating socket (DGRAM is data gram, how UDP works)
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind(('192.168.1.142', 2000 + IP_NO))
#serverSock.bind(('192.168.0.101', UDP_PORT_NO))

# Establish the node 
# (the name of the node will end with the port number, ex: 'K4_Comm_3000' for port 3000)
rospy.init_node('K4_Send_Cmd_' + str(IP_NO), anonymous=True)

# Initialize angular(W) and linear(V) velocity control variables
W = 0
V = 0

Trig = False
msg = K4_controls()
addr = ('192.168.1.' + str(IP_NO), 2000)

"""
def callback(data):
	# Log angular and linear velocity controls
	rospy.loginfo(data)
	global W, V
	W = data.ctrl_W
	V = data.ctrl_V
	serverSock.sendto(str(W) + 'x' + str(V), addr)
"""
last_data = K4_controls()
started = False

def callback(data):
    # print "New message received"
    global started, last_data
    last_data = data
    if (not started):
        started = True

def timer_callback(event):
    global started, last_data
    global W, V
    if (started):
		#rospy.loginfo(last_data)
		W = last_data.ctrl_W
		V = last_data.ctrl_V
		serverSock.sendto(str(W) + 'x' + str(V), addr)


def send_cmd():
	s = rospy.Subscriber('K4_controls_' + var, K4_controls, callback)
	timer = rospy.Timer(rospy.Duration(0.01), timer_callback)
	rospy.spin()
	timer.shutdown()

if __name__ == '__main__':
	try:
		send_cmd()
	except rospy.ROSInterruptException:
		pass