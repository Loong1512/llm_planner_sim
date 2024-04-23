#!/usr/bin/env python
import rospy
from llm_grabbing_bringup.camera_image_subscriber import CameraImageSubscriber
import cv2
from cv_bridge import CvBridge, CvBridgeError
from PIL import Image as PILImage, ImageDraw
import torch
from transformers import OwlViTProcessor, OwlViTForObjectDetection, Owlv2Processor, Owlv2ForObjectDetection
import matplotlib.pyplot as plt
import numpy as np
import tf2_ros
import tf2_geometry_msgs
from geometry_msgs.msg import PointStamped
from transformers.utils.constants import OPENAI_CLIP_MEAN, OPENAI_CLIP_STD

objects = ["yellow block", "blue block"]

camera_image_subscriber = CameraImageSubscriber()
bridge = CvBridge()

def get_all_obj_pos(objects):
    rospy.sleep(1)
    rgb_image = camera_image_subscriber.get_rgb_image()
    depth_image = camera_image_subscriber.get_depth_image()
    objects_point = object_detect(rgb_image, depth_image, objects)
    points_in_camera = transform_to_camera_link(objects_point)
    return transform_to_base_link(points_in_camera)
    

def object_detect(rgb_image, depth_image, objects):
    try:
        # 将ROS图像消息转换为OpenCV图像
        cv_rgb_image = bridge.imgmsg_to_cv2(rgb_image, "bgr8")
        cv_depth_image = bridge.imgmsg_to_cv2(depth_image, "16UC1")
    except CvBridgeError as e:
        print(e)

    pil_image = PILImage.fromarray(cv2.cvtColor(cv_rgb_image, cv2.COLOR_BGR2RGB))

    # Load the model and processor
    # local_model_path = "/home/long/.cache/huggingface/hub/models--google--owlvit-base-patch32/snapshots/cbc355fb364588351c5d51c7f74465e8e7ec6f72"
    # processor = OwlViTProcessor.from_pretrained(local_model_path)
    # model = OwlViTForObjectDetection.from_pretrained(local_model_path)

    local_model_path = "/home/long/.cache/huggingface/hub/models--google--owlv2-base-patch16-ensemble/snapshots/7c77fc1316a353da3109f81d80ae118dd58fd55b"
    processor = Owlv2Processor.from_pretrained(local_model_path)
    model = Owlv2ForObjectDetection.from_pretrained(local_model_path)

    texts = [objects]
    inputs = processor(text=texts, images=pil_image, return_tensors="pt")

    # with torch.no_grad():
    outputs = model(**inputs)

    def get_preprocessed_image(pixel_values):
        pixel_values = pixel_values.squeeze().numpy()
        unnormalized_image = (pixel_values * np.array(OPENAI_CLIP_STD)[:, None, None]) + np.array(OPENAI_CLIP_MEAN)[:, None, None]
        unnormalized_image = (unnormalized_image * 255).astype(np.uint8)
        unnormalized_image = np.moveaxis(unnormalized_image, 0, -1)
        unnormalized_image = PILImage.fromarray(unnormalized_image)
        return unnormalized_image

    unnormalized_image = get_preprocessed_image(inputs.pixel_values)

    # Convert outputs (bounding boxes and class logits) to COCO API
    target_sizes = torch.Tensor([unnormalized_image.size[::-1]])
    results = processor.post_process_object_detection(outputs=outputs, target_sizes=target_sizes, threshold=0.2)
    i = 0  # Retrieve predictions for the first image for the corresponding text queries
    text = texts[i]
    boxes, scores, labels = results[i]["boxes"], results[i]["scores"], results[i]["labels"]

    objects_point = {}
    objects_score = {}
    for box, score, label in zip(boxes, scores, labels):
        box = [round(i, 2) for i in box.tolist()]
        score = round(score.item(), 3)
        object_name = text[label]
        print(f"Detected {text[label]} with confidence {score} at location {box}")
        if object_name not in objects_score or score > objects_score[object_name]:
            objects_score[object_name] = score
            box_center_x = (box[0] + box[2]) / 2 * 640 / 960
            box_center_y = (box[1] + box[3]) / 2 * 480 / 720
            # box_center_depth = 300
            box_center_depth = cv_depth_image[int(box_center_y), int(box_center_x)]
            box_center_point = [box_center_x, box_center_y, box_center_depth]
            objects_point[object_name] = box_center_point

    # Visualize the detection results
    visualized_image = unnormalized_image.copy()

    draw = ImageDraw.Draw(visualized_image)

    for box, score, label in zip(boxes, scores, labels):
        box = [round(i, 2) for i in box.tolist()]
        x1, y1, x2, y2 = tuple(box)
        draw.rectangle(xy=((x1, y1), (x2, y2)), outline="red")
        draw.text(xy=(x1, y1), text=text[label])
        draw.text(xy=(x1, y1 - 10), text=str(round(score.item(), 3)))

    visualized_image.show()
    
    # plot_predictions(unnormalized_image, text, scores, boxes, labels)
    print("objects_point: ", objects_point)
    return objects_point

def plot_predictions(pil_image, text, scores, boxes, labels):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10)) 
    ax.imshow(pil_image, extent=[0, 960, 960, 0]) 
    ax.set_axis_off()

    for score, box, label in zip(scores, boxes, labels):
        top_left_x, top_left_y, bottom_right_x, bottom_right_y = [round(i, 2) for i in box.tolist()]
        ax.plot([top_left_x, bottom_right_x, bottom_right_x, top_left_x, top_left_x],
                [top_left_y, top_left_y, bottom_right_y, bottom_right_y, top_left_y], "r")
        ax.text(
            top_left_x,
            bottom_right_y + 0.015,
            f"{text[label]}: {score:1.2f}",
            ha="left",
            va="top",
            color="red",
            bbox={
                "facecolor": "white",
                "edgecolor": "red",
                "boxstyle": "square,pad=.3"
            })
    plt.show()

def transform_to_camera_link(objects_point):
    points_in_camera = []
    # asus xtion pro live内参
    # camera_matrix = np.array([[590.43761, 0, 330.69402],
    #                         [0, 591.66, 242.16509],
    #                         [0, 0, 1]])

    # realsence d435内参
    camera_matrix = np.array([[604.4634399414062, 0, 315.8777160644531],
                        [0, 602.7150268554688, 246.13929748535156],
                        [0, 0, 1]])

    # 将图像坐标转换为相机坐标
    inv_camera_matrix = np.linalg.inv(camera_matrix)

    points_in_camera = {}
    for object_name, object_point in objects_point.items():
        image_point = np.array([object_point[0], object_point[1], 1])
        camera_point = object_point[2] * np.dot(inv_camera_matrix, image_point) / 1000.0
        points_in_camera[object_name] = camera_point.tolist()

    print("Points in camera_link:", points_in_camera)
    return points_in_camera

def transform_to_base_link(points_in_camera):
    object_positions = {}
    for object_name, point_in_camera in points_in_camera.items():
        # 创建TF2缓冲区和监听器
        tf_buffer = tf2_ros.Buffer()
        listener = tf2_ros.TransformListener(tf_buffer)

        # 等待TF缓冲区填充
        rospy.sleep(1)

        # 从camera_link到wrist_3_link的转换
        try:
            transform_camera_to_wrist = tf_buffer.lookup_transform('wrist_3_link', 'camera_link', rospy.Time(), rospy.Duration(1.0))
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as ex:
            rospy.logerr('Error getting transform from camera_link to wrist_3_link: %s' % ex)
            exit(1)

        # 定义camera_link下的坐标点
        camera_point = PointStamped()
        camera_point.header.frame_id = 'camera_link'
        camera_point.point.x = point_in_camera[0]
        camera_point.point.y = point_in_camera[1]
        camera_point.point.z = point_in_camera[2]

        # 将点从camera_link转换到wrist_3_link
        point_in_wrist = tf2_geometry_msgs.do_transform_point(camera_point, transform_camera_to_wrist)

        # 从wrist_3_link到base_link的转换
        try:
            transform_wrist_to_base = tf_buffer.lookup_transform('base_link', 'wrist_3_link', rospy.Time(), rospy.Duration(1.0))
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as ex:
            rospy.logerr('Error getting transform from wrist_3_link to base_link: %s' % ex)
            exit(1)

        # 将点从wrist_3_link转换到base_link
        point_in_base = tf2_geometry_msgs.do_transform_point(point_in_wrist, transform_wrist_to_base)

        object_positions[object_name] = point_in_base.point

    print("Object positions in base_link:", object_positions)
    return object_positions


rospy.sleep(1)
rgb_image = camera_image_subscriber.get_rgb_image()
depth_image = camera_image_subscriber.get_depth_image()
objects_point = object_detect(rgb_image, depth_image, objects)
points_in_camera = transform_to_camera_link(objects_point)
all_obj_pos = transform_to_base_link(points_in_camera)
print("all_obj_pos: ", all_obj_pos)


def query_obj_position(obj):
    return all_obj_pos[obj]