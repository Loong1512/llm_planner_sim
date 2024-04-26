from geometry_msgs.msg import Point

obj_ori_loc_dict = {
    "eraser": (-0.060578, 0.348331, 1.015129),
    "storage box": (-0.231700, 0.480407, 1.026760),
    "coffee cup": (7, 8, 9),
    "coffee machine": (10, 11, 12),
    "bowl": (13, 14, 15),
    "coke can": (16, 17, 18),
    "paper cup": (19, 20, 21),
    "trash bin": (22, 23, 24)
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
    position_dict = {}
    for key, value in obj_base_loc_dict.items():
        if object in key:
            position_dict[key] = value
    return position_dict

def distance(p1: Point, p2: Point):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)**0.5