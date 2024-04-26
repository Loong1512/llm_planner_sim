from llm_grabbing_bringup.LMP import LMP
import numpy as np
# from llm_grabbing_bringup.controller_utils import reset_to_default_pose
# from llm_grabbing_bringup.perception_utils import get_all_obj_pos
from llm_grabbing_bringup.action_lib import move_to_position, reset_to_default_pose, close_gripper, open_gripper
from llm_grabbing_bringup.env import query_obj_position

class LMP_interface():
  
  # # ======================================================
  # # == functions exposed to LLM
  # # ======================================================
  # def get_obj_name(self):
  #   return self.object_names[::]
  
  def move_to_position(self, x, y, z):
    return move_to_position(x, y, z)
  
  def query_obj_position(self, obj):
    return query_obj_position(obj)
  
  def reset_to_default_pose(self):
    return reset_to_default_pose()
  
  def close_gripper(self):
    return close_gripper()
  
  def open_gripper(self):
    return open_gripper()


def setup_LMP(general_config, debug=False):
  lmps_config = general_config['lmp_config']['lmps']
  # LMP env wrapper
  lmp_env = LMP_interface()
  # creating APIs that the LMPs can interact with
  fixed_vars = {
      'np': np
  }  # external library APIs
  variable_vars = {
      k: getattr(lmp_env, k)
      for k in dir(lmp_env) if callable(getattr(lmp_env, k)) and not k.startswith("_")
  }  # our custom APIs exposed to LMPs

  variable_vars['say'] = lambda msg: print(f'robot says: {msg}')

  # allow LMPs to access other LMPs   parse_query_obj
  lmp_names = [name for name in lmps_config.keys() if not name in ['composer', 'planner', 'config']]
  low_level_lmps = {
      k: LMP(k, lmps_config[k], fixed_vars, variable_vars, debug)
      for k in lmp_names
  }
  variable_vars.update(low_level_lmps)

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
  lmps.update(low_level_lmps)

  return lmps