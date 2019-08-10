#!/usr/bin/env python

#!/usr/bin/env python
# license removed for brevity
import rospy
import math
import time
import rosnode
# Import message file
from std_msgs.msg import String
from khepera_communicator.msg import K4_controls, SensorReadings
from geometry_msgs.msg import TransformStamped

start = time.time()

rospy.init_node('Central_Algorithm', anonymous=True)

# Get all the node names for all the currently running K4_Send_Cmd nodes (all running Kheperas)
node_list = rosnode.get_node_names()
#print node_list

# Find the topics that contains the "Sensor_Readings_" title
khep_node_list = [s for s in node_list if "K4_Send_Cmd_" in s]
ip_num_list = [x[13:16] for x in khep_node_list]
khep_node_cnt = len(khep_node_list)

#print "Number of sensor reading topics: ", khep_node_cnt
# print "All sensor readings topics: ", khep_topic_list
#print khep_node_list
#print ip_num_list

pub = []
for i in range(khep_node_cnt):
	pub.append(rospy.Publisher('K4_controls_' + str(ip_num_list[i]), K4_controls, queue_size = 10))


def callback(data, args):
	i = args
	control_msgs = K4_controls()
	control_msgs.ctrl_W = data.transform.translation.x
	control_msgs.ctrl_V = data.transform.translation.x * 100
	#rospy.loginfo(control_msgs)
	pub[i].publish(control_msgs)

def central():
	
	sub = []

	for i in range(khep_node_cnt):
		sub.append(rospy.Subscriber('vicon/k' + ip_num_list[i] + '/k' + ip_num_list[i], TransformStamped, callback, i ))

	rospy.spin()


if __name__ == '__main__':
	try:
		central()
	except rospy.ROSInterruptException:
		pass