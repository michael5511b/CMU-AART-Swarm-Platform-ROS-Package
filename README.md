# Advance-Agent-Swarm-Platform-ROS-Package
The ROS package for the swarm platform/system at the Advanced Agent Robotics Technology Lab of CMU.

- Name: Michael Cheng
- Programming Languages: C for Khepera scripts, Python for ROS scripts
- OS: Ubuntu 18.04 for ROS and the Khepera, Windows for the Vicon System

## Instructions:
**1.** Make sure ROS is on your computer.

**2.** Download the vicon_bridge package from "https://github.com/ethz-asl/vicon_bridge" to your workspace.

**3.** Make sure you have the common messages package in your workspace. If not, download it because we need the geometry_msgs message type.

**4.** To implement your swarm algorithm to the system, open Central_Algorithm.py in the khepera_communicator folder with your favorite editor, and modify the content in the callback function, that is where your algorithms should be implemented.

**5.** If the khepera control script is not in the khepera already, navigate to the khepera_scripts folder on your computer, type in "scp template root@KHEPERA'sIP:/home/root" in the terminal to send the control script "template" to the Khepera.

**6.** If you want to modify the control script on the Khepera, you will have to follow the instruction manual of the Khepera IV to download and install the libkhepera library and the light toolchain. You can modify the prog-template.c file with an editor, make the file with the pocky compiler, and scp the new template make file to the Khepera.

**7.** In the Vicon Tracker software, create an object for each Khepera robot (Learn how to use the Tracker software from the tutorials), and name the object with "k + last three digits of the IP address of the Khepera robot". Ex: for the Khepera with an IP of 192.168.1.150, name the Vicon Tracker object as "k150".

**8.** Remember to activate UDP communication in the Vicon Tracker. Follow the README instructions in the vicon_bridge package for more detail on configuring your system.

**9.** Run roscore in the terminal to start ROS.

**10.** Input "roslaunch vicon_bridge vicon.launch" in the terminal to start the vicon_bridge ROS node.

**11.** For each Khepera we want to run, input "rosrun khepera_communicator K4_Send_Cmd.py" in the terminal, it will ask you for the last three digits of the IP address for each Khepera.

**12.** SSH into each Khepera, and run the "template" script using the command "./template".

**13.** When you are ready to run the Kheperas, input "rosrun khepera_communicator Central_Algorithm.py", and watch your algorithm come to life!
