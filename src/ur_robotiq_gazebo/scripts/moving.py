#!/usr/bin/env python
import sys
import moveit_commander
import rospy
from gazebo_ros_link_attacher.srv import SetStatic, SetStaticRequest, SetStaticResponse
from gazebo_ros_link_attacher.srv import Attach, AttachRequest, AttachResponse

setstatic_srv = rospy.ServiceProxy("/link_attacher_node/setstatic", SetStatic)
attach_srv = rospy.ServiceProxy("/link_attacher_node/attach", Attach)
detach_srv = rospy.ServiceProxy("/link_attacher_node/detach", Attach)
setstatic_srv.wait_for_service()
attach_srv.wait_for_service()
detach_srv.wait_for_service()

def initialize_moveit_commander():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('ecnu_moveit_script', anonymous=True)

def get_move_group(group_name):
    return moveit_commander.MoveGroupCommander(group_name)


def go_to_up_position():
    arm_group = get_move_group("arm")
    arm_group.set_named_target("up")
    arm_group.go(wait=True)
    arm_group.stop()  # Ensure no residual movement
    arm_group.clear_pose_targets()

def go_to_position_0():
    arm_group = get_move_group("arm")
    # Assuming this is the correct order after checking with get_active_joints()
    joint_order = ["elbow_joint", "shoulder_lift_joint", "shoulder_pan_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
    joint_values = [-1.039479762839365, -2.098557688377362, 0.2290678071995762, -1.513969420685819, 1.5346515393408557, -1.5671462265974867]

    joint_target = dict(zip(joint_order, joint_values))
    arm_group.set_joint_value_target(joint_target)
    arm_group.go(wait=True)
    arm_group.stop()
    arm_group.clear_pose_targets()


def go_to_position_1():
    arm_group = get_move_group("arm")
    # Assuming this is the correct order after checking with get_active_joints()
    joint_order = ["elbow_joint", "shoulder_lift_joint", "shoulder_pan_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
    joint_values = [-1.120108013858106, -2.239695266503033, 0.19366570065995514, -1.5257283258207046, 1.5354224189167889, -1.572204145081738]

    # Blue Cup [-1.4998782863153584, -2.0276680851487017, 0.22919242844010412, -1.3333105597837243, 1.5352867489086748, -1.5697730319594365]

    joint_target = dict(zip(joint_order, joint_values))
    arm_group.set_joint_value_target(joint_target)
    arm_group.go(wait=True)
    arm_group.stop()
    arm_group.clear_pose_targets()


def half_close():
      
    gripper_group = get_move_group("gripper")
    # Assuming 'finger_joint' is the correct name within your configuration
    finger_joint_name = "finger_joint"
    finger_joint_position = 0.5  # Target position for half-close
    
    # Set the target position for the finger_joint
    gripper_group.set_joint_value_target({finger_joint_name: finger_joint_position})
    gripper_group.go(wait=True)

    
    
    rospy.loginfo("Creating ServiceProxy to /link_attacher_node/attach")
    attach_srv = rospy.ServiceProxy('/link_attacher_node/attach',
                                    Attach)
    attach_srv.wait_for_service()
    rospy.loginfo("Created ServiceProxy to /link_attacher_node/attach")
    req = AttachRequest()
    req.model_name_1 = "Dummy_Cup"
    req.link_name_1 = "link_1"
    req.model_name_2 = "robot"
    req.link_name_2 = "wrist_3_link"
    attach_srv.call(req)

def go_to_position_lift():
    arm_group = get_move_group("arm")
    # Assuming this is the correct order after checking with get_active_joints()
    joint_order = ["elbow_joint", "shoulder_lift_joint", "shoulder_pan_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
    joint_values = [-1.5147659181367192, -1.6037309143662277, 0.2293622794200214, -1.341779726809058, 1.535823738638114, -1.5714179506534443]
    
    joint_target = dict(zip(joint_order, joint_values))
    arm_group.set_joint_value_target(joint_target)
    arm_group.go(wait=True)
    arm_group.stop()
    arm_group.clear_pose_targets()


def go_to_position_sink():
    arm_group = get_move_group("arm")
    # Assuming this is the correct order after checking with get_active_joints()
    joint_order = ["elbow_joint", "shoulder_lift_joint", "shoulder_pan_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
    joint_values =  [-0.7072442626105433, -2.4265703228006297, -0.6511724014821567, -1.352159407178764, 1.5375515023838346, -1.5693515403086211]
    joint_target = dict(zip(joint_order, joint_values))
    arm_group.set_joint_value_target(joint_target)
    arm_group.go(wait=True)
    arm_group.stop()
    arm_group.clear_pose_targets()

def go_to_position_sinkDown():
    arm_group = get_move_group("arm")
    # Assuming this is the correct order after checking with get_active_joints()
    joint_order = ["elbow_joint", "shoulder_lift_joint", "shoulder_pan_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
    joint_values =  [-1.0028255700340996,-2.627704235231831, -0.6510476730161683, -1.349910549421768, 1.537554320399951, -1.5738603029628306]
    
    joint_target = dict(zip(joint_order, joint_values))
    arm_group.set_joint_value_target(joint_target)
    arm_group.go(wait=True)
    arm_group.stop()
    arm_group.clear_pose_targets()


def open_gripper():
    req = AttachRequest()
    req.model_name_1 = "Dummy_Cup"
    req.link_name_1 = "link_1"
    req.model_name_2 = "robot"
    req.link_name_2 = "wrist_3_link"
    detach_srv.call(req)

    gripper_group = get_move_group("gripper")
    gripper_group.set_named_target("open")
    gripper_group.go(wait=True)
    gripper_group.stop()  # Ensure no residual movement
    gripper_group.clear_pose_targets()



def close_gripper():
    gripper_group = get_move_group("gripper")
    gripper_group.set_named_target("close")
    gripper_group.go(wait=True)
    gripper_group.stop()  # Ensure no residual movement
    gripper_group.clear_pose_targets()

if __name__ == "__main__":
    initialize_moveit_commander()
    
       
    print("Moving the arm to the up position...")
    go_to_up_position() 
    open_gripper()
    
    print("Moving the arm to the ready0")
    go_to_position_0()

    print("Moving the arm to the ready1")
    go_to_position_1()

    half_close()  

    go_to_position_lift()

    go_to_position_sink()

    # go_to_position_sinkDown()

    open_gripper()




   
    # Remember to shut down MoveIt cleanly
    moveit_commander.roscpp_shutdown()
