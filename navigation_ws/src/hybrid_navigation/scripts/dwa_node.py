#!/usr/bin/env python3
import rospy
import numpy as np
from geometry_msgs.msg import Point, PointStamped
from visualization_msgs.msg import Marker
from std_msgs.msg import Float32MultiArray

class DWAArrowNode:
    def __init__(self):
        rospy.init_node("dwa_arrow_node")

        self.histogram = None
        self.goal = Point(5.0, 0.0, 0.0)  # Objetivo fijo por ahora
        self.position = Point(0.0, 0.0, 0.0)  # Posición simulada
        self.yaw = 0.0  # Orientación simulada

        rospy.Subscriber("/vfh/histogram", Float32MultiArray, self.hist_callback)
        self.arrow_pub = rospy.Publisher("/dwa_arrow_marker", Marker, queue_size=1)

        self.timer = rospy.Timer(rospy.Duration(0.5), self.timer_callback)
        rospy.loginfo("Nodo DWA con flecha inicializado")

    def hist_callback(self, msg):
        self.histogram = np.array(msg.data)

    def timer_callback(self, event):
        if self.histogram is None:
            return

        best_angle = self.calculate_best_angle()
        if best_angle is not None:
            self.publish_arrow(best_angle)

    def calculate_best_angle(self):
        safe_threshold = 1.0
        front_sector = len(self.histogram) // 2

        safe_sectors = [i for i, d in enumerate(self.histogram) if d > safe_threshold]
        if not safe_sectors:
            return None

        angles = [((i - front_sector) * (2*np.pi / len(self.histogram))) for i in safe_sectors]
        scores = [-abs(a) + 0.1*np.cos(a) for a in angles]  # Ejemplo simple

        best_idx = np.argmax(scores)
        return angles[best_idx]

    def publish_arrow(self, angle):
        length = 1.0
        arrow = Marker()
        arrow.header.frame_id = "base_link"
        arrow.header.stamp = rospy.Time.now()
        arrow.ns = "dwa"
        arrow.id = 0
        arrow.type = Marker.ARROW
        arrow.action = Marker.ADD
        arrow.scale.x = 1.0
        arrow.scale.y = 0.1
        arrow.scale.z = 0.1
        arrow.color.r = 0.0
        arrow.color.g = 1.0
        arrow.color.b = 0.0
        arrow.color.a = 1.0

        start = Point(0, 0, 0)
        end = Point(length * np.cos(angle), length * np.sin(angle), 0)
        arrow.points = [start, end]

        self.arrow_pub.publish(arrow)

if __name__ == '__main__':
    try:
        node = DWAArrowNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

