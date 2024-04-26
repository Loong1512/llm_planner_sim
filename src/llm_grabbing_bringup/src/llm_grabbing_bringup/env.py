from geometry_msgs.msg import Point

obj_ori_loc_dict = {
    "eraser": (-0.060578, 0.348331, 1.015129),
    "storage box": (-0.231700, 0.480407, 1.126760),
    "coffee cup": (7, 8, 9),
    "coke can": (16, 17, 18),
    "paper cup": (19, 20, 21),
    "trash bin": (22, 23, 24),
    "yellow block": (0.068211, 0.449849, 1.040000),
    "red block": (0.300505, 0.671873, 1.057720),
    "plate_1": (0.239931, 0.663077, 1.014610),
    "plate_2": (-0.129726, 0.657167, 1.015800),
}

obj_base_loc_dict = {} 
for obj_name, loc in obj_ori_loc_dict.items():
    base_loc = Point()
    base_loc.x = loc[0]
    base_loc.y = loc[1]
    base_loc.z = loc[2] - 1.02 + 0.17
    obj_base_loc_dict[obj_name] = base_loc


def query_obj_position(object: str):
    print(f"### {object} is at {obj_base_loc_dict[object]} ###")
    return obj_base_loc_dict[object]

def query_obj_positions(object: str):
    position_list = []
    for key, value in obj_base_loc_dict.items():
        if object in key:
            position_list.append(value)
    return position_list

def distance(p1: Point, p2: Point):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)**0.5