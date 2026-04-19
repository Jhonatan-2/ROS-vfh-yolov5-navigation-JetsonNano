#!/usr/bin/env python3
import rospy
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import Header
from hybrid_navigation.msg import Detection, DetectionArray
import torch
import math
from message_filters import ApproximateTimeSynchronizer, Subscriber
import time
import cv2

class RealTimeYOLONode:
    def __init__(self):
        rospy.init_node('realtime_yolo_node')
        
        # Configuración de hardware
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        rospy.loginfo(f"Usando dispositivo: {self.device}")
        
        # Carga optimizada del modelo YOLOv5
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True, autoshape=True).to(self.device)
        self.model.conf = 0.5  # Umbral de confianza
        self.model.iou = 0.45   # Umbral de NMS
        self.model.classes = None  # Todas las clases
        
        # Configuración de la cámara
        self.h_fov = math.radians(90)  # Campo de visión horizontal en radianes
        self.frame_skip = 2            # Procesar 1 de cada 2 frames (balance calidad/rendimiento)
        
        # Sincronización RGB-D con buffer circular
        rgb_sub = Subscriber('/zed2i/zed_node/rgb/image_rect_color', Image, buff_size=2**24)
        depth_sub = Subscriber('/zed2i/zed_node/depth/depth_registered', Image, buff_size=2**24)
        
        self.ts = ApproximateTimeSynchronizer(
            [rgb_sub, depth_sub],
            queue_size=20,
            slop=0.05,  # 50ms de tolerancia
            allow_headerless=True
        )
        self.ts.registerCallback(self.sync_callback)
        
        # Publicadores
        self.det_pub = rospy.Publisher('/yolo/detections', DetectionArray, queue_size=1)
        self.debug_pub = rospy.Publisher('/yolo/debug_image', Image, queue_size=1)
        
        # Métricas de rendimiento
        self.frame_counter = 0
        self.processing_times = []
        self.last_time = time.time()
        
        # Warm-up del modelo
        self.warm_up_model()
        rospy.loginfo("Nodo YOLOv5 en tiempo real listo")

    def warm_up_model(self):
        """Ejecuta inferencias iniciales para estabilizar el modelo"""
        dummy_input = torch.randn(1, 3, 640, 640).to(self.device)
        for _ in range(3):
            _ = self.model(dummy_input)
        torch.cuda.empty_cache()

    def process_image_pair(self, rgb_msg, depth_msg):
        """Procesamiento optimizado del par RGB-D"""
        try:
            # Conversión a NumPy optimizada
            rgb_img = np.frombuffer(rgb_msg.data, dtype=np.uint8)
            rgb_img = rgb_img.reshape(rgb_msg.height, rgb_msg.width, -1)[..., :3]  # Forzar 3 canales
            
            depth_img = np.frombuffer(depth_msg.data, dtype=np.float32)
            depth_img = depth_img.reshape(depth_msg.height, depth_msg.width)
            
            # Preprocesamiento de imagen (optimizado)
            #rgb_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR)  # YOLO espera BGR
            
            # Inferencia con el modelo
            with torch.no_grad():  # Deshabilita gradientes para inferencia
                results = self.model(rgb_img)
            
            # Post-procesamiento
            detections = DetectionArray()
            detections.header = Header(
                stamp=rospy.Time.now(),
                frame_id=rgb_msg.header.frame_id
            )
            
            for *xyxy, conf, cls in results.xyxy[0].cpu().numpy():
                det = self.create_detection(xyxy, conf, cls, depth_img)
                detections.detections.append(det)
            
            # Publicar imagen de debug (opcional)
            self.publish_debug_image(results.render()[0], rgb_msg.header)
            
            return detections
            
        except Exception as e:
            rospy.logerr(f"Error en process_image_pair: {str(e)}")
            return None

    def create_detection(self, xyxy, conf, cls, depth_img):
        """Crea un mensaje Detection optimizado"""
        detection = Detection()
        detection.class_id = int(cls)
        detection.class_name = self.model.names[int(cls)]
        detection.confidence = float(conf)
        
        # Cálculo del centro del bounding box
        x_center, y_center = map(int, [(xyxy[0] + xyxy[2])/2, (xyxy[1] + xyxy[3])/2])
        detection.bbox_center_x = float(x_center)
        detection.bbox_center_y = float(y_center)
        
        # Cálculo de distancia y ángulo con verificación de límites
        if (0 <= x_center < depth_img.shape[1] and 0 <= y_center < depth_img.shape[0]):
            distance = depth_img[y_center, x_center]
            detection.distance = float(distance) if np.isfinite(distance) else 0.0
            detection.angle = float((x_center - depth_img.shape[1]/2) * (self.h_fov / depth_img.shape[1]))
        else:
            detection.distance = 0.0
            detection.angle = 0.0
            
        return detection

    def publish_debug_image(self, image, header):
        """Publica imagen con detecciones para debugging"""
        try:
            if self.debug_pub.get_num_connections() > 0:
                debug_msg = Image()
                debug_msg.header = header
                debug_msg.height = image.shape[0]
                debug_msg.width = image.shape[1]
                debug_msg.encoding = "bgr8"
                debug_msg.step = image.shape[1] * 3
                debug_msg.data = image.tobytes()
                self.debug_pub.publish(debug_msg)
        except Exception as e:
            rospy.logwarn(f"No se pudo publicar imagen debug: {str(e)}")

    def sync_callback(self, rgb_msg, depth_msg):
        """Callback sincronizado optimizado"""
        self.frame_counter += 1
        if self.frame_counter % self.frame_skip != 0:
            return
            
        start_time = time.time()
        
        detections = self.process_image_pair(rgb_msg, depth_msg)
        if detections and len(detections.detections) > 0:
            self.det_pub.publish(detections)
            
        # Métricas de rendimiento
        proc_time = time.time() - start_time
        self.processing_times.append(proc_time)
        
        if self.frame_counter % 20 == 0:
            avg_time = np.mean(self.processing_times[-20:])
            rospy.loginfo_throttle(
                1.0,
                f"Detecciones: {len(detections.detections) if detections else 0} | "
                f"FPS: {1/avg_time:.1f} | "
                f"Latencia: {avg_time*1000:.1f}ms"
            )

    def shutdown_hook(self):
        """Método de limpieza al apagar el nodo"""
        rospy.loginfo("Liberando recursos...")
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        node = RealTimeYOLONode()
        rospy.on_shutdown(node.shutdown_hook)
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Apagado del nodo YOLO")
    except Exception as e:
        rospy.logerr(f"Error crítico: {str(e)}")
