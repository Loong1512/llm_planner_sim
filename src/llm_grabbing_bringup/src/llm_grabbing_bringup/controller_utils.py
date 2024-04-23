# #!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose
import sys
import math
import moveit_commander
import moveit_msgs.msg
from robotiq_2f_gripper_control.msg import Robotiq2FGripper_robot_output
import tf.transformations as tfs
import numpy as np

moveit_commander.roscpp_initialize(sys.argv)

# 初始化MoveIt!的命令组
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
move_group = moveit_commander.MoveGroupCommander("manipulator")
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=10)

# 创建发布者，发布Robotiq2FGripper_robot_output消息
pub = rospy.Publisher('Robotiq2FGripperRobotOutput', Robotiq2FGripper_robot_output, queue_size=10)

# 等待发布者建立
rospy.sleep(1.0)

def reset_to_default_pose():
    joint_goal = move_group.get_current_joint_values()
    print("current joint values: ", joint_goal)
    # ori = tfs.quaternion_from_euler(math.radians(180), 0, 0)
    q = np.deg2rad([120, -120, 110, -180, -90, 0])
    # joint_goal[0] = -1.134
    # joint_goal[1] = -0.974
    # joint_goal[2] = -1.266
    # joint_goal[3] = -1.818
    # joint_goal[4] = 1.641
    # joint_goal[5] = 0.070
    move_group.go(joint_goal, wait=True)
    move_group.stop()

def move_to_position(target_position):
    waypoints = []

    # 设置目标点
    goal_pose = Pose()
    goal_pose.position.x = target_position[0]
    goal_pose.position.y = target_position[1]
    goal_pose.position.z = target_position[2]
    goal_pose.orientation.x = 0.95036
    goal_pose.orientation.y = 0.17131
    goal_pose.orientation.z = -0.091838
    goal_pose.orientation.w = -0.42753
    waypoints.append(goal_pose)

    # 进行笛卡尔路径规划
    (plan, fraction) = move_group.compute_cartesian_path(waypoints, 0.1, 0.0)
    move_group.execute(plan, wait=True)
    rospy.sleep(5)

def control_gripper(position, speed, force):
    """
    控制Robotiq夹抓的函数。
    :param position: 夹抓的目标位置（0-255，0完全开，255完全闭合）。
    :param speed: 夹抓的速度（0-255）。
    :param force: 夹抓的力量（0-255）。
    """
    # 创建Robotiq2FGripper_robot_output消息
    command = Robotiq2FGripper_robot_output()
    command.rACT = 1
    command.rGTO = 1
    command.rPR = position
    command.rSP = speed
    command.rFR = force

    # 发布夹抓命令
    pub.publish(command)

def close_gripper():
    try:
        # 控制夹抓操作
        # 例如：闭合夹抓，速度和力量中等
        control_gripper(255, 150, 100)

        # 延时以确保命令发送
        rospy.sleep(2.0)
    except rospy.ROSInterruptException:
        pass

def open_gripper():
    control_gripper(0, 150, 150)
    rospy.sleep(2.0)

# def move_to_joint_position(self, )

