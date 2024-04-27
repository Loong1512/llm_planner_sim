import sys
import rospy
import moveit_commander
import rospy
import numpy as np
from gazebo_ros_link_attacher.srv import Attach, AttachRequest
from geometry_msgs.msg import Pose


attach_srv = rospy.ServiceProxy("/link_attacher_node/attach", Attach)
detach_srv = rospy.ServiceProxy("/link_attacher_node/detach", Attach)
attach_srv.wait_for_service()
detach_srv.wait_for_service()

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('ecnu_moveit_script', anonymous=True)

def get_move_group(group_name):
    return moveit_commander.MoveGroupCommander(group_name)

def move_to_position(x, y, z):
    arm_group = get_move_group("arm")
    current_pose = arm_group.get_current_pose().pose

    waypoints = []

    # 设置目标点
    goal_pose = Pose()
    goal_pose.position.x = x
    goal_pose.position.y = y
    goal_pose.position.z = z
    goal_pose.orientation.x = current_pose.orientation.x
    goal_pose.orientation.y = current_pose.orientation.y
    goal_pose.orientation.z = current_pose.orientation.z
    goal_pose.orientation.w = current_pose.orientation.w
    waypoints.append(goal_pose)

    # 进行笛卡尔路径规划
    (plan, fraction) = arm_group.compute_cartesian_path(waypoints, 0.1, 0.0)
    print("### compute_cartesian_path success ###")
    arm_group.execute(plan, wait=True)
    arm_group.stop()
    arm_group.clear_pose_targets()


# def move_to_position(object: str):
#     arm_group = get_move_group("arm")
#     joint_order = ["shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
#     if object == "default" :
#         joint_values = [-1.57, -1.57, -1.57, -1.57, 1.57, -1.57]
#     elif object == "hammer" :
#         joint_values =  [np.deg2rad(-44), np.deg2rad(-103), np.deg2rad(-120) , np.deg2rad(-47), np.deg2rad(90), np.deg2rad(-44)]
#     elif object == "yellow_cube_4" :
#         joint_values =  [np.deg2rad(-90), np.deg2rad(-102), np.deg2rad(-117) , np.deg2rad(-50), np.deg2rad(90), np.deg2rad(-90)]
#     elif object == "yellow_cube_4_top" :
#         joint_values =  [np.deg2rad(-112), np.deg2rad(-106), np.deg2rad(-99) , np.deg2rad(-65), np.deg2rad(90), np.deg2rad(-112)]
#     elif object == "yellow_cube_4_end" :
#         joint_values =  [np.deg2rad(-112), np.deg2rad(-113), np.deg2rad(-106) , np.deg2rad(-52), np.deg2rad(90), np.deg2rad(-112)]
#     elif object == "green_cup" :
#         joint_values =  [np.deg2rad(-96), np.deg2rad(-98), np.deg2rad(-113) , np.deg2rad(-59), np.deg2rad(90), np.deg2rad(-12)]
#     elif object == "green_bowl_top" :
#         joint_values =  [np.deg2rad(-54), np.deg2rad(-94), np.deg2rad(-88) , np.deg2rad(-90), np.deg2rad(90), np.deg2rad(35)]
#     elif object == "green_bowl" :
#         joint_values =  [np.deg2rad(-54), np.deg2rad(-94), np.deg2rad(-116) , np.deg2rad(-60), np.deg2rad(90), np.deg2rad(35)]
#     elif object == "coke_can" :
#         joint_values =  [np.deg2rad(-60), np.deg2rad(-64), np.deg2rad(-137) , np.deg2rad(-72), np.deg2rad(90), np.deg2rad(-70)]
#     elif object == "number3_top" :
#         joint_values =  [np.deg2rad(-82), np.deg2rad(-130), np.deg2rad(-42) , np.deg2rad(-99), np.deg2rad(90), np.deg2rad(-84)]
#     elif object == "number3" :
#         joint_values =  [np.deg2rad(-82), np.deg2rad(-130), np.deg2rad(-58) , np.deg2rad(-84), np.deg2rad(90), np.deg2rad(-84)]
#     elif object == "yellow_box_1" :
#         joint_values =  [np.deg2rad(-78), np.deg2rad(-92), np.deg2rad(-128) , np.deg2rad(-51), np.deg2rad(90), np.deg2rad(-82)]
#     elif object == "yellow_box_1_top" :
#         joint_values =  [np.deg2rad(-92), np.deg2rad(-85), np.deg2rad(-122) , np.deg2rad(-63), np.deg2rad(90), np.deg2rad(-92)]
#     elif object == "red_box" :
#         joint_values =  [np.deg2rad(-80), np.deg2rad(-107), np.deg2rad(-110) , np.deg2rad(-53), np.deg2rad(90), np.deg2rad(-80)]
#     elif object == "red_box_top" :
#         joint_values =  [np.deg2rad(-68), np.deg2rad(-103), np.deg2rad(-102) , np.deg2rad(-66), np.deg2rad(90), np.deg2rad(-70)]
#     elif object == "yellow_box_0" :
#         joint_values =  [np.deg2rad(-82), np.deg2rad(-123), np.deg2rad(-87) , np.deg2rad(-62), np.deg2rad(90), np.deg2rad(-86)]
#     elif object == "yellow_box_0_top" :
#         joint_values =  [np.deg2rad(-91), np.deg2rad(-120), np.deg2rad(-76) , np.deg2rad(-75), np.deg2rad(90), np.deg2rad(-91)]
#     else:
#         raise NotImplementedError()
#     joint_target = dict(zip(joint_order, joint_values))
#     arm_group.set_joint_value_target(joint_target)
#     arm_group.go(wait=True)
#     arm_group.stop()

# def close_gripper(object: str):
#     gripper_group = get_move_group("gripper")
#     # Assuming 'finger_joint' is the correct name within your configuration
#     finger_joint_name = "finger_joint"
#     finger_joint_position = 0.36
#     # finger_joint_position = 0.5  # Target position for half-close
#     # Set the target position for the finger_joint
#     gripper_group.set_joint_value_target({finger_joint_name: finger_joint_position})
#     gripper_group.set_max_velocity_scaling_factor(1)
#     gripper_group.go(wait=True)
#     gripper_group.stop()  # Ensure no residual movement

#     req = AttachRequest()
#     req.model_name_1 = object
#     req.link_name_1 = "link"
#     req.model_name_2 = "robot"
#     req.link_name_2 = "wrist_3_link"
#     attach_srv.call(req)


# def open_gripper(object: str):
#     req = AttachRequest()
#     req.model_name_1 = object
#     req.link_name_1 = "link"
#     req.model_name_2 = "robot"
#     req.link_name_2 = "wrist_3_link"
#     detach_srv.call(req)

#     gripper_group = get_move_group("gripper")
#     gripper_group.set_named_target("open")
#     gripper_group.set_max_velocity_scaling_factor(1)
#     gripper_group.go(wait=True)
#     gripper_group.stop()  # Ensure no residual movement
#     gripper_group.clear_pose_targets()

def reset_to_default_pose():
    arm_group = get_move_group("arm")
    # joint_order = ["shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
    # joint_values = [-1.57, -1.57, -1.57, -1.57, 1.57, -1.57]
    # joint_target = dict(zip(joint_order, joint_values))
    arm_group.set_named_target("default")
    arm_group.go(wait=True)
    arm_group.stop()
    arm_group.clear_pose_targets()

def close_gripper(name, link_name, joint_value):

    # # test1
    # name = 'eraser'
    # size = 0.36

    # # test2 test4
    # name = 'yellow_box'
    # size = 0.36

    gripper_group = get_move_group("gripper")
    finger_joint_name = "finger_joint"
    gripper_group.set_joint_value_target({finger_joint_name: joint_value})
    gripper_group.set_max_velocity_scaling_factor(1)
    gripper_group.go(wait=True)
    gripper_group.stop()
    gripper_group.clear_pose_targets()

    req = AttachRequest()
    req.model_name_1 = name
    req.link_name_1 = link_name
    req.model_name_2 = "robot"
    req.link_name_2 = "wrist_3_link"
    attach_srv.call(req)

def open_gripper(name, link_name):

    # # test1
    # name = 'eraser'

    # # test2 test4
    # name = 'yellow_box'

    req = AttachRequest()
    req.model_name_1 = name
    req.link_name_1 = link_name
    req.model_name_2 = "robot"
    req.link_name_2 = "wrist_3_link"
    detach_srv.call(req)

    gripper_group = get_move_group("gripper")
    gripper_group.set_named_target("open")
    gripper_group.set_max_velocity_scaling_factor(1)
    gripper_group.go(wait=True)
    gripper_group.stop()
    gripper_group.clear_pose_targets()