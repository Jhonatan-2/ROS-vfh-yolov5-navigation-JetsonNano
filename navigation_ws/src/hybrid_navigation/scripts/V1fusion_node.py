#!/usr/bin/env python3
import rospy
import numpy as np
from std_msgs.msg import Float32MultiArray, String
from hybrid_navigation.msg import DetectionArray
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point

class FusionNode:
    def __init__(self):
        rospy.init_node('fusion_node')
        self.last_angles = []
        # Parámetros configurables
        self.safety_distance = 1.0  # Distancia mínima segura (metros)
        self.robot_width = 0.3      # Ancho del robot + margen (metros)
        self.forward_threshold = np.radians(5)  # ±15° se considera "frente"
        
        # Suscriptores
        rospy.Subscriber('/vfh/histogram', Float32MultiArray, self.hist_callback)
        rospy.Subscriber('/yolo/detections', DetectionArray, self.det_callback)
        
        # Publicador
        self.cmd_pub = rospy.Publisher('/cmd_direction', String, queue_size=1)
        
        # Variables de estado
        self.current_hist = None
        self.dynamic_obstacles = []
        self.last_cmd = "stop"
        
        rospy.loginfo("Nodo de fusión inicializado")

    def hist_callback(self, msg):
        """Almacena el último histograma VFH"""
        self.current_hist = np.array(msg.data)

    def det_callback(self, msg):
        """Procesa las detecciones de YOLO"""
        try:
            self.dynamic_obstacles = []
            for det in msg.detections:
                if det.distance < self.safety_distance and det.distance > 0:
                    self.dynamic_obstacles.append({
                        'angle': det.angle,
                        'distance': det.distance
                    })
            self.publish_command()  # ¡Sin argumentos!
        except Exception as e:
            rospy.logerr(f"Error en det_callback: {str(e)}")

    def combine_obstacles(self):
        """Combina obstáculos estáticos y dinámicos"""
        if self.current_hist is None:
            return None
            
        danger_map = self.current_hist.copy()
        
        for obstacle in self.dynamic_obstacles:
            angle_deg = np.degrees(obstacle['angle'])
            sector = int((angle_deg + 180) / (360 / len(danger_map))) % len(danger_map)
            # Penalización progresiva (no bloqueo total)
            danger_map[sector] = min(danger_map[sector], obstacle['distance'] * 0.3)  # 0.3 es factor de peso
                        
        return danger_map



    def calculate_best_angle(self, danger_map):
        if danger_map is None:
            return None
        
        # 1. Configuración de ángulos y pesos
        angles = np.linspace(-np.pi, np.pi, len(danger_map), endpoint=False)
        sector_width = 2 * np.pi / len(danger_map)
        
        # 2. Cálculo de pesos con prioridad izquierda
        weights = np.zeros_like(danger_map)
        for i in range(len(danger_map)):
            if danger_map[i] > self.safety_distance:
                # Prioriza sectores izquierdos (ángulos negativos)
                angle = angles[i]
                weights[i] = (1.0 + 0.3 * (-angle/np.pi))  # +50% peso a la izquierda
                
        # 3. Validación y cálculo
        if np.sum(weights) == 0:
            return None
            
        best_angle = np.average(angles, weights=weights)
        
        # 4. Aplicar límites y suavizado
        clamped_angle = np.clip(best_angle, -np.pi/2, np.pi/2)  # ±90° máximo
        
        # Debug: Imprime los sectores con mayor peso
        top_sectors = np.argsort(weights)[-3:]
        rospy.logdebug(f"Sectores preferidos: {top_sectors}, Pesos: {weights[top_sectors]}")
        
        return clamped_angle * 0.7

    def publish_command(self):
        try:
            # 1. Verificar datos de entrada
            if self.current_hist is None:
                rospy.logwarn("Esperando datos del histograma VFH...")
                return
                
            # 2. Combinar obstáculos con comprobación
            danger_map = self.combine_obstacles()
            if danger_map is None:
                rospy.logwarn("No se pudo generar mapa de peligro")
                self._publish_safe_command("stop")
                return
                
            # 3. Calcular ángulo con validación
            best_angle = self.calculate_best_angle(danger_map)
            if best_angle is None:
                rospy.loginfo("¡Peligro! No hay rutas seguras → Comando: stop")
                self._publish_safe_command("stop")
                return
                
            # 4. Determinar comando
            if abs(best_angle) <= self.forward_threshold:
                cmd = "forward"
            elif best_angle > 0:
                cmd = "right"
            else:
                cmd = "left"
                
            rospy.loginfo(f"Ángulo óptimo: {np.degrees(best_angle):.1f}° → Comando: {cmd}")
            self._publish_safe_command(cmd)
            
        except Exception as e:
            rospy.logerr(f"Error crítico en publish_command: {str(e)}")
            self._publish_safe_command("stop")

    def _publish_safe_command(self, cmd):
        """Publica comandos con verificación de estado"""
        if cmd != self.last_cmd:
            msg = String()
            msg.data = cmd
            self.cmd_pub.publish(msg)
            self.last_cmd = cmd

    
if __name__ == '__main__':
    try:
        node = FusionNode()
        
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Nodo de fusión detenido")
    except Exception as e:
        rospy.logerr(f"Error fatal: {str(e)}")
