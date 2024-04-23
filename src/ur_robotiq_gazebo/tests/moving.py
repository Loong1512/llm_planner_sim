#!/usr/bin/env python
import sys
import moveit_commander
import rospy
from std_msgs.msg import Float64MultiArray
from moveit_msgs.msg import Grasp, PickupAction, PickupGoal, PickupResult, MoveItErrorCodes

def initialize_moveit_commander():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('ecnu_moveit_script', anonymous=True)

def get_move_group(group_name):
    return moveit_commander.MoveGroupCommander(group_name)

def print_joint_order(group_name):
    group = get_move_group(group_name)
    joint_names = group.get_active_joints()  # or group.get_joints() depending on what you need
    print(f"Joint order for {group_name}: {joint_names}")

def command_finger_joint_effort(finger_effort):
    pub = rospy.Publisher('/joint_group_eff_controller/command', Float64MultiArray, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz
    
    effort_command = Float64MultiArray()
    # Initialize all other efforts to zero, adjust as necessary for your application
    efforts = [0, finger_effort, 0, 0, 0, 0, 0]
    effort_command.data = efforts

    start_time = rospy.get_time()
    while (rospy.get_time() - start_time) < duration:
        rospy.loginfo("Publishing effort command with finger effort")
        pub.publish(effort_command)
        rate.sleep()


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
    finger_joint_position = 0.65  # Target position for half-close
    
    # Set the target position for the finger_joint
    gripper_group.set_joint_value_target({finger_joint_name: finger_joint_position})
    gripper_group.go(wait=True)
  
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

def go_to_position_lift():
    arm_group = get_move_group("arm")
    # Assuming this is the correct order after checking with get_active_joints()
    joint_order = ["elbow_joint", "shoulder_lift_joint", "shoulder_pan_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
    joint_values = [-1.5147659181367192, -1.6037309143662277, 0.2293622794200214, -1.341779726809058, 1.535823738638114, -1.5714179506534443]
    
    # Set the maximum acceleration scaling factor for the arm_group
    arm_group.set_max_velocity_scaling_factor(0.1)# Adjust this value as necessary
        
    gripper_group = get_move_group("gripper")
    gripper_group.set_named_target("close")
    
    # Set target position for the arm
    joint_target = dict(zip(joint_order, joint_values))
    arm_group.set_joint_value_target(joint_target)
    
    # Execute the motion
    arm_group.go(wait=True)
    arm_group.stop()  # Ensure no residual movement
    arm_group.clear_pose_targets()

def go_to_position_sink():
    arm_group = get_move_group("arm")
    # Assuming this is the correct order after checking with get_active_joints()
    joint_order = ["elbow_joint", "shoulder_lift_joint", "shoulder_pan_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
    joint_values =  [-0.6874730898050885, -2.416361107295316, -0.7920126136260359, -1.3408227879174106, 1.5358306838028222, -1.5713440464938104]

    joint_target = dict(zip(joint_order, joint_values))
    arm_group.set_joint_value_target(joint_target)
    arm_group.go(wait=True)
    arm_group.stop()
    arm_group.clear_pose_targets()


def open_gripper():
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
    print_joint_order("arm")

    # try:
    #     # Set your desired effort here
    #     desired_effort = -0.5  # Adjust this value based on your requirements and safety considerations
    #     command_finger_joint_effort(desired_effort)
    # except rospy.ROSInterruptException:
    #     pass




    
    # print("Moving the arm to the up position...")
    go_to_up_position() 
    open_gripper()
    
    print("Moving the arm to the ready0")
    go_to_position_0()

    print("Moving the arm to the ready1")
    go_to_position_1()

    half_close()

    go_to_position_lift()

    # go_to_position_sink()

    # open_gripper()




   
    # Remember to shut down MoveIt cleanly
    moveit_commander.roscpp_shutdown()
