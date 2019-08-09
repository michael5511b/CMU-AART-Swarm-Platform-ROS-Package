#!/usr/bin/env python
import rospy
# from std_msgs.msg import String
from geometry_msg.msg import TransformStamped

def callback(data):
  rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def listener():

  rospy.init_node('listener', anonymous=True)
  rospy.Subscriber("vicon/k150/k150", TransformStamped, callback)

  rospy.spin()

if __name__ == '__main__':
  listener()