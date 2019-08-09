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




"""
def __init__(self):
	self.W = 0
	self.V = 0
"""
Time_val_khepera = []
khepera_freq = []
t_old_khepera   = -1

W = 0
V = 0

def callback(data):
	rospy.loginfo(data)
	global W 
	W = data.ctrl_W
	global V 
	V = data.ctrl_V

def K4_Comm():
	# Server socket port
	UDP_PORT_NO = 3000

	# creating socket (DGRAM is data gram, how UDP works)
	serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	serverSock.bind(('192.168.1.142', UDP_PORT_NO))

	"""
	pub_acc = rospy.Publisher('Accelerometer', Acc, queue_size=10)
	pub_gyro = rospy.Publisher('Gyroscope', Gyro, queue_size=10)
	pub_pos = rospy.Publisher('EncoderPosition', Encoder_POS, queue_size=10)
	pub_spd = rospy.Publisher('EncoderSpeed', Encoder_SPD, queue_size=10)
	pub_time = rospy.Publisher('Time', Time, queue_size=10)
	"""

	pub = rospy.Publisher('Sensor_Readings', SensorReadings, queue_size=10)
	msg = SensorReadings()

	"""
	msg_acc = Acc()
	msg_gyro = Gyro()
	msg_pos = Encoder_POS()
	msg_spd = Encoder_SPD()
	msg_t = Time()

	msg_t.time = 0

	msg_acc.acc_x = 0
	msg_acc.acc_y = 0
	msg_acc.acc_z = 0

	msg_gyro.gyro_x = 0
	msg_gyro.gyro_y = 0
	msg_gyro.gyro_z = 0

	msg_pos.pos_L = 0
	msg_pos.pos_R = 0
	msg_spd.spd_L = 0
	msg_spd.spd_R = 0
	"""
	TM = 0
	t_new = 0

	rospy.init_node('K4_Communicator', anonymous=True)
    #rate = rospy.Rate(10) # 10hz
	start = time.time()
	while(t_new <= 30.0):
		end = time.time()
		t_new = end-start
		if TM == 0:
			TM = TM + 1
		else:
			serverSock.settimeout(1)
		data, addr = serverSock.recvfrom(1024)

		T = data.split('T')[1]

		AX = data.split('AX')[1]
		AY = data.split('AY')[1]
		AZ = data.split('AZ')[1]

		GX = data.split('GX')[1]
		GY = data.split('GY')[1]
		GZ = data.split('GZ')[1]

		PL = data.split('PL')[1]
		PR = data.split('PR')[1]

		SL = data.split('SL')[1]
		SR = data.split('SR')[1]

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


		rospy.loginfo(msg)    		
   		pub.publish(msg)

		t_new_khepera = float(T)
   		khepera_freq.append(1 / (t_new_khepera - t_old_khepera))
   		Time_val_khepera.append(t_new_khepera)
		sub = rospy.Subscriber('K4_controls', K4_controls, callback)

		serverSock.sendto(str(W) + 'x' + str(V), addr)

        #rospy.spin()

    


	serverSock.sendto('0x0', addr)
	serverSock.close()
	plt.figure(1)

	#plt.plot(Time_val_python, python_freq,'-r') 
	plt.plot(Time_val_khepera, khepera_freq,'-b') 
	#plt.title('A tale of 6 subplots')
	plt.ylabel('Khepera Frequency (Hz)')
	plt.xlabel('Time')
	plt.grid()
	plt.show()



if __name__ == '__main__':
	try:
		K4_Comm()
	except rospy.ROSInterruptException:
		pass