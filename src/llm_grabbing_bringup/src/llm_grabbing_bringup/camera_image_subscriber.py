#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image

class CameraImageSubscriber:
    def __init__(self):
        self.rgb_image = None
        self.depth_image = None

        rospy.init_node('camera_image_subscriber')
        rospy.Subscriber("/camera/color/image_raw", Image, self.rgb_image_callback)
        rospy.Subscriber("/camera/depth/image_rect_raw", Image, self.depth_image_callback)

    def rgb_image_callback(self, data):
        self.rgb_image = data

    def get_rgb_image(self):
        return self.rgb_image
    
    def depth_image_callback(self, data):
        self.depth_image = data

    def get_depth_image(self):
        return self.depth_image
