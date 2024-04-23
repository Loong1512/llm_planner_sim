## Installation

First install the reuqired packges

```
rosdep install --from-paths src --ignore-src -r -y
```
Please double-check if this is the right one?

## Usage
To start the simulation:
```
roslaunch ur_robotiq_gazebo ur5_bringup.launch 
```
The start the Moveit control
```
roslaunch ecnu_moveit_config demo.launch 
```

## Modification
Do bring up the world environment only:
```
roslaunch ur_robotiq_gazebo my_world.launch 
```

