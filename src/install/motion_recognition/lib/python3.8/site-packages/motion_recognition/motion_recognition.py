import rclpy
from rclpy.node import Node

from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import Int8

import numpy as np


class RGBToGrayConverter(Node):
    def __init__(self):
        super().__init__("convert_node")
        self.get_logger().info("Starting work")
        self.subscriber = self.create_subscription(Image, "/image_raw", self.listener_callback, 10)
        # self.publisher = self.create_publisher(Int8, "/motion_flag", 10)
        self.publisher = self.create_publisher(String, 'chatter', 10)
        self.bridge = CvBridge()
        # My Work
        self.prev_kadr = []
        self.current_kadr = []
        # My Work

    def _check_motion(self, img):
        # TODO: implement algorithm here
        # My Work
        move = 0 # 0 - not move, 1 = move 

        if(len(prev_kadr) == 0): #first call of function
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            prev_kadr = cv2.blur(gray, (5, 5))

        else: #non first call of function
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            current_kadr = cv2.blur(gray, (5, 5))

            difference = cv2.subtract(current_kadr, prev_kadr)

            mask = cv2.threshold(difference, 20, 255, cv2.THRESH_BINARY)[1]

            percentage = (np.count_nonzero(mask) * 100)/ mask.size # number of non zero pixel / imsize, for 640*480 imsize = 307200

            if percentage >= 0.1: #number non zero pixel more? than 307.2
                move = 1

            prev_kadr = current_kadr
        # My Work

        self.get_logger().info("Got image with shape: %s" % str(img.shape))
        return move # original 0, also my work

    def listener_callback(self, msg: Image):
        img_from_cam = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        motion_flag = self._check_motion(img_from_cam)

        # msg = Int8()
        msg = String()
        # msg.data = int(motion_flag)
        msg.data = str(motion_flag)

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    print("Subscriber created")
    convert_node = RGBToGrayConverter()
    rclpy.spin(convert_node)
    print("Spin")
    convert_node.destroy_node()
    print("Destroied")
    rclpy.shutdown()


if __name__ == "__main__":
    main()
