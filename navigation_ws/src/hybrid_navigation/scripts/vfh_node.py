#!/usr/bin/env python3
import rospy
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray, String
from std_srvs.srv import Trigger, TriggerResponse
import math
import threading

class VFHNode:
    def __init__(self):
        rospy.init_node('vfh_node', log_level=rospy.INFO)
        
        # Configuración de parámetros
        self.min_dist = rospy.get_param('~min_dist', 0.3)  # 30cm
        self.max_dist = rospy.get_param('~max_dist', 5.0)  # 5m
        self.num_sectors = rospy.get_param('~num_sectors', 72)  # 5° por sector
        
        # Publicador para el nodo de fusión
        self.hist_pub = rospy.Publisher('/vfh/histogram', Float32MultiArray, queue_size=10)
        
        # Publicador adicional para visualización simplificada
        self.viz_pub = rospy.Publisher('/vfh/viz', String, queue_size=1)
        
        # Suscriptor de profundidad
        self.depth_sub = rospy.Subscriber('/zed2i/zed_node/depth/depth_registered', 
                                         Image, 
                                         self.depth_callback,
                                         queue_size=1,
                                         buff_size=2**24)
        
        # Variable de control para parada limpia
        self.running = True
        
        # Iniciar hilo para visualización en terminal
        self.viz_thread = threading.Thread(target=self.terminal_visualization)
        self.viz_thread.daemon = True
        self.viz_thread.start()
        
        # Servicio para parada remota (CORREGIDO)
        self.stop_service = rospy.Service('~stop_vfh', Trigger, self.handle_stop)
        
        rospy.loginfo("Nodo VFH inicializado. Enviando datos a /vfh/histogram")
        rospy.loginfo("Use 'rosservice call /vfh_node/stop_vfh' para detener el nodo")

    def depth_callback(self, msg):
        if not self.running:
            return
            
        try:
            # Convertir imagen de profundidad
            depth_img = np.frombuffer(msg.data, dtype=np.float32).reshape(msg.height, msg.width)
            
            # Calcular histograma polar
            histogram = self.calculate_polar_histogram(depth_img)
            
            # Publicar para el nodo de fusión
            hist_msg = Float32MultiArray()
            hist_msg.data = histogram.tolist()
            self.hist_pub.publish(hist_msg)
            
            # Publicar versión simplificada para visualización
            self.publish_viz_data(histogram)
            
        except Exception as e:
            rospy.logerr(f"Error en procesamiento: {str(e)}")

    def calculate_polar_histogram(self, depth_img):
        h, w = depth_img.shape
        center_x, center_y = w // 2, h // 2
        
        # Crear grids de coordenadas
        y, x = np.indices((h, w))
        dx = x - center_x
        dy = y - center_y
        
        # Calcular ángulos de -180° a 180°
        angles = np.degrees(np.arctan2(dy, dx))  # Eliminamos % 360
        valid_mask = (depth_img > self.min_dist) & (depth_img < self.max_dist) & np.isfinite(depth_img)
        
        # Convertir ángulos a sectores (0 a 71)
        angle_step = 360 / self.num_sectors
        angles_wrapped = (angles + 180) % 360  # Mapear a [0°, 360°)
        sectors = (angles_wrapped[valid_mask] // angle_step).astype(int)
        
        # Asegurar que los sectores estén en el rango correcto
        sectors = np.clip(sectors, 0, self.num_sectors - 1)
        valid_depths = depth_img[valid_mask]
        
        # Crear histograma
        histogram = np.full(self.num_sectors, self.max_dist)
        if len(sectors) > 0:
            np.minimum.at(histogram, sectors, valid_depths)
            
        return histogram

    def publish_viz_data(self, histogram):
        """Publica datos simplificados para visualización"""
        # Encontrar el sector con el obstáculo más cercano
        min_dist = np.min(histogram)
        min_sector = np.argmin(histogram)
        angle = min_sector * (360 / self.num_sectors)
        
        # Crear representación ASCII simple
        viz_str = String()
        viz_str.data = f"[VFH] Obstáculo más cercano: {min_dist:.2f}m en {angle:.1f}° | " + \
                      "".join(['.' if d > self.max_dist*0.8 else 'X' for d in histogram])
        
        self.viz_pub.publish(viz_str)

    def terminal_visualization(self):
        """Muestra datos en la terminal"""
        rate = rospy.Rate(2)  # 2 Hz para no saturar la terminal
        while not rospy.is_shutdown() and self.running:
            try:
                # Podrías subscribirte a tu propio topic /vfh/viz aquí
                # o acceder directamente a los últimos datos
                rate.sleep()
            except:
                break

    def handle_stop(self, req):
        """Maneja la solicitud de parada del servicio"""
        self.running = False
        rospy.loginfo("Recibida solicitud de parada. Deteniendo nodo...")
        return TriggerResponse(True, "VFH detenido correctamente")

    def run(self):
        """Bucle principal"""
        rospy.on_shutdown(self.shutdown)
        rate = rospy.Rate(10)  # 10 Hz
        
        while not rospy.is_shutdown() and self.running:
            rate.sleep()

    def shutdown(self):
        """Limpieza al apagar"""
        rospy.loginfo("Apagando nodo VFH...")
        self.running = False

if __name__ == '__main__':
    try:
        node = VFHNode()
        node.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("Nodo VFH apagado por interrupción ROS")
    except Exception as e:
        rospy.logerr(f"Error en nodo VFH: {str(e)}")
    finally:
        rospy.loginfo("Nodo VFH terminado")