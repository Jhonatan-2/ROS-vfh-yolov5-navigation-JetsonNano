#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray
from hybrid_navigation.msg import Detection, DetectionArray
from time import sleep

def publish_detection(pub, class_id, class_name, confidence, distance, angle):
    msg = DetectionArray()
    msg.detections.append(
        Detection(
            class_id=class_id,
            class_name=class_name,
            confidence=confidence,
            bbox_center_x=320,
            bbox_center_y=240,
            distance=distance,
            angle=angle
        )
    )
    pub.publish(msg)

def publish_histogram(pub, values):
    msg = Float32MultiArray(data=values)
    pub.publish(msg)

if __name__ == "__main__":
    rospy.init_node("test_fusion_node")

    yolo_pub = rospy.Publisher("/yolo/detections", DetectionArray, queue_size=1)
    vfh_pub = rospy.Publisher("/vfh/histogram", Float32MultiArray, queue_size=1)

    sleep(1)  # Espera a que los publishers se conecten

    rospy.loginfo("🧪 Test 1: Escenario libre con silla a la derecha")
    publish_histogram(vfh_pub, [5.0]*70)  # Todo libre
    publish_detection(yolo_pub, 56, "chair", 0.9, 1.0, 0.5)  # Objeto a la derecha
    sleep(2)

    rospy.loginfo("🧪 Test 2: Obstáculo frontal estático")
    publish_histogram(vfh_pub, [5.0]*33 + [0.2] + [5.0]*36)  # Valle al centro
    publish_detection(yolo_pub, 56, "chair", 0.9, 1.0, 0.5)  # Mismo objeto
    sleep(2)

    rospy.loginfo("🧪 Test 3: Obstáculo frontal dinámico (persona)")
    publish_histogram(vfh_pub, [5.0]*70)  # Todo libre
    publish_detection(yolo_pub, 0, "person", 0.95, 0.5, 0.0)  # Persona al frente
    sleep(2)

    rospy.loginfo("🧪 Test 4: Zona libre a la izquierda")
    publish_histogram(vfh_pub, [5.0]*10 + [0.3]*5 + [5.0]*55)  # Obstáculo a la izquierda
    publish_detection(yolo_pub, 0, "person", 0.85, 0.7, -0.8)
    sleep(2)

    rospy.loginfo("✅ Pruebas completas.")

