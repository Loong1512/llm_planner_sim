from llm_grabbing_bringup.LMP import LMP
import numpy as np
# from llm_grabbing_bringup.controller_utils import reset_to_default_pose
# from llm_grabbing_bringup.perception_utils import get_all_obj_pos
from llm_grabbing_bringup.action_lib import move_to_position, reset_to_default_pose, close_gripper, open_gripper
from llm_grabbing_bringup.env import query_obj_position, query_obj_positions
from geometry_msgs.msg import Point


class LMP_interface():
  def __init__(self, name_list, link_name_list, joint_value_list):
    self.count = 0
    self.name_list = name_list
    self.link_name_list = link_name_list
    self.joint_value_list = joint_value_list
  
  # # ======================================================
  # # == functions exposed to LLM
  # # ======================================================
  # def get_obj_name(self):
  #   return self.object_names[::]
  
  def move_to_position(self, x, y, z):
    return move_to_position(x, y, z)
  
  def query_obj_position(self, obj):
    return query_obj_position(obj)
  
  def query_obj_positions(self, obj):
    return query_obj_positions(obj)
  
  def reset_to_default_pose(self):
    return reset_to_default_pose()
  
  def close_gripper(self):
    link_name = self.link_name_list[self.count]
    joint_value = self.joint_value_list[self.count]
    name = self.name_list[self.count]
 
    return close_gripper(name, link_name, joint_value)
  
  def open_gripper(self):
    link_name = self.link_name_list[self.count]
    name = self.name_list[self.count]

    self.count += 1
    return open_gripper(name, link_name)
  
  def distance(self, p1: Point, p2: Point):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)**0.5


def setup_LMP(test_name, general_config, debug=False):
  lmps_config = general_config['lmp_config']['lmps']
  env_config = general_config['lmp_config']['env'][test_name]
  # LMP env wrapper
  lmp_env = LMP_interface(list(env_config['name']), list(env_config['link_name']), list(env_config['joint_value']))
  # creating APIs that the LMPs can interact with
  fixed_vars = {
      'np': np
  }  # external library APIs
  variable_vars = {
      k: getattr(lmp_env, k)
      for k in dir(lmp_env) if callable(getattr(lmp_env, k)) and not k.startswith("_")
  }  # our custom APIs exposed to LMPs

  # variable_vars['say'] = lambda msg: print(f'robot says: {msg}')

  # # allow LMPs to access other LMPs   parse_query_obj
  # lmp_names = [name for name in lmps_config.keys() if not name in ['composer', 'planner', 'config']]
  # low_level_lmps = {
  #     k: LMP(k, lmps_config[k], fixed_vars, variable_vars, debug)
  #     for k in lmp_names
  # }
  # variable_vars.update(low_level_lmps)

  # creating the LMP for skill-level composition
  composer = LMP(
      'composer', lmps_config['composer'], fixed_vars, variable_vars, debug
  )
  variable_vars['composer'] = composer

  # creating the LMP that deals w/ high-level language commands
  task_planner = LMP(
      'planner', lmps_config['planner'], fixed_vars, variable_vars, debug
  )

  lmps = {
      'plan_ui': task_planner,
      'composer_ui': composer,
  }
  # lmps.update(low_level_lmps)

  return lmps