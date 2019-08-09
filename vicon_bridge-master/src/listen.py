#!/usr/bin/env python
import rospy
from geometry_msgs.msg import TransformStamped

def callback(data):
  rospy.loginfo(data)
def listener():

  rospy.init_node('listener', anonymous=True)
  rospy.Subscriber("vicon/k150/k150", TransformStamped, callback)

  rospy.spin()

if __name__ == '__main__':
  listener()