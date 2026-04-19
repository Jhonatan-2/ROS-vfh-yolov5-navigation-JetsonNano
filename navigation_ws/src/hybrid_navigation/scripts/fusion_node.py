#!/usr/bin/env python3
import rospy
import numpy as np
from std_msgs.msg import Float32, Float32MultiArray, String
from hybrid_navigation.msg import DetectionArray

class FusionNode:
    def __init__(self):
        rospy.init_node('fusion_node')
        
        # Configuración de parámetros
        self.safety_distance = rospy.get_param('~safety_distance', 0.50)  # 1m
        self.robot_width = rospy.get_param('~robot_width', 0.3)          # 30cm
        self.forward_threshold = np.radians(rospy.get_param('~forward_threshold', 5))  # ±5°
        self.left_bias = rospy.get_param('~left_bias', 0.1)              # Sesgo izquierdo (0-1)
        
        # Suscriptores
        rospy.Subscriber('/vfh/histogram', Float32MultiArray, self.hist_callback)
        rospy.Subscriber('/yolo/detections', DetectionArray, self.det_callback)
        
        # Publicadores
        self.cmd_pub = rospy.Publisher('/cmd_direction', String, queue_size=1)
        self.angle_pub = rospy.Publisher('/cmd_angle', Float32, queue_size=1)
        self.danger_pub = rospy.Publisher('/fusion/danger_map', Float32MultiArray, queue_size=1)

        # Estado del sistema
        self.current_hist = None
        self.dynamic_obstacles = []
        self.last_cmd = "stop"
        self.last_valid_cmd = "stop"
        self.angle_history = []
        self.current_danger_map = None
        
        rospy.loginfo("Nodo de fusión inicializado con parámetros:")
        rospy.loginfo(f"• Distancia segura: {self.safety_distance}m")
        rospy.loginfo(f"• Umbral frontal: ±{np.degrees(self.forward_threshold):.1f}°")
        rospy.loginfo(f"• Sesgo izquierdo: {self.left_bias}")

    def hist_callback(self, msg):
        """Procesa histograma VFH"""
        try:
            self.current_hist = np.array(msg.data)
            self.publish_command()
        except Exception as e:
            rospy.logerr(f"Error en hist_callback: {str(e)}")

    def det_callback(self, msg):
        """Procesa detecciones YOLO"""
        try:
            self.dynamic_obstacles = [
                {'angle': det.angle, 'distance': det.distance}
                for det in msg.detections
                if 0 < det.distance < self.safety_distance
            ]
            self.publish_command()
        except Exception as e:
            rospy.logerr(f"Error en det_callback: {str(e)}")

    def publish_danger_map(self):
        """Publica el mapa de peligro actual como Float32MultiArray"""
        if self.current_danger_map is None:
            return
            
        try:
            # Crear mensaje ROS
            msg = Float32MultiArray()
            
            # Convertir numpy array a lista de Python
            msg.data = self.current_danger_map.tolist()
            
            # Publicar
            self.danger_pub.publish(msg)
            rospy.logdebug(f"Publicado danger_map con {len(msg.data)} elementos")
            
        except Exception as e:
            rospy.logerr(f"Error al publicar danger_map: {str(e)}")

    def combine_obstacles(self):
        if self.current_hist is None:
            return None
            
        danger_map = self.current_hist.copy()
        
        for ob in self.dynamic_obstacles:
            angle_deg = np.degrees(ob['angle'])
            sector = int((angle_deg + 180) / (360 / len(danger_map))) % len(danger_map)
            
            # Penalización principal + vecinos cercanos
            danger = ob['distance'] * 0.25  # Valor base
            
            for delta in range(-1, 2):  # Solo sectores adyacentes (±1)
                idx = (sector + delta) % len(danger_map)
                danger_map[idx] = min(danger_map[idx], danger)

        

        return danger_map

    def calculate_best_angle(self, danger_map):
        if danger_map is None:
            return None

        # 1. Detección frontal más estricta (ángulo ±15°)
        front_range = int(len(danger_map) * 15/360)  # N° de sectores para ±15°
        front_sectors = range(len(danger_map)//2 - front_range, 
                            len(danger_map)//2 + front_range + 1)
        
        if any(danger_map[i] < self.safety_distance * 0.7 for i in front_sectors):
            rospy.logwarn("Obstáculo frontal detectado - forzando STOP")
            return None

        # 2. Cálculo de pesos mejorado
        angles = np.linspace(-np.pi, np.pi, len(danger_map), endpoint=False)
        safety_mask = danger_map > self.safety_distance
        
        # 2.1 Priorizar dirección actual (reducir giros bruscos)
        forward_bias = np.cos(angles)**2  # Máximo en 0° (frente)
        
        # 2.2 Combinar con left_bias
        weights = np.where(
            safety_mask,
            (1.0 + self.left_bias * (angles/np.pi)) * forward_bias,
            0
        )

        if np.sum(weights) == 0:
            return None

        # 3. Suavizado más agresivo
        best_angle = np.average(angles, weights=weights)
        self.angle_history.append(best_angle)
        self.angle_history = self.angle_history[-3:]  # Ventana más pequeña
        
        return np.clip(np.mean(self.angle_history), -np.pi/3, np.pi/3)  # ±60° máximo

    def _create_dummy_histogram(self):
        """Genera histograma temporal basado en YOLO"""
        dummy_hist = np.full(72, self.safety_distance * 1.5)  # 72 sectores (5° cada uno)
        
        for ob in self.dynamic_obstacles:
            angle_deg = np.degrees(ob['angle'])
            sector = int((angle_deg + 180) / 5) % 72
            
            # Aplicar patrón de peligro radial
            for delta in range(-3, 4):  # ±10°
                idx = (sector + delta) % 72
                danger = ob['distance'] * 0.3  # Factor configurable
                dummy_hist[idx] = min(dummy_hist[idx], danger)
                
        return dummy_hist

    def publish_command(self):
        """Lógica principal de toma de decisiones"""
        try:
            
        

            # Caso 1: Fusión completa
            if self.current_hist is not None and self.dynamic_obstacles:
                danger_map = self.combine_obstacles()
                self.current_danger_map = danger_map
                best_angle = self.calculate_best_angle(danger_map)
                
            # Caso 2: Solo obstáculos estáticos
            elif self.current_hist is not None:
                rospy.logwarn_throttle(5, "Usando solo datos VFH (YOLO inactivo)")
                self.current_danger_map = self.current_hist.copy()
                best_angle = self.calculate_best_angle(self.current_hist.copy())
                
            # Caso 3: Solo obstáculos dinámicos
            elif self.dynamic_obstacles:
                rospy.logwarn_throttle(5, "Usando solo datos YOLO (VFH inactivo)")
                danger_map = self._create_dummy_histogram()
                self.current_danger_map = danger_map
                best_angle = self.calculate_best_angle(self._create_dummy_histogram())
                
            # Caso 4: Sin datos
            else:
                rospy.logwarn_throttle(5, "Esperando datos de sensores...")
                self._publish_last_valid_cmd()
                return
            
            if self.current_danger_map is not None:
                self.publish_danger_map()

            self._publish_final_command(best_angle)
            
        except Exception as e:
            rospy.logerr(f"Error en publish_command: {str(e)}")
            self._publish_safe_stop()

    def _publish_final_command(self, best_angle):
        """Traduce ángulo a comando y publica"""
        if best_angle is None:
            cmd = "stop"
            rospy.loginfo("¡Peligro! No hay rutas seguras → Comando: stop")
        else:
            angle_deg = np.degrees(best_angle)
            
            if abs(angle_deg) <= np.degrees(self.forward_threshold):
                cmd = "forward"
            elif angle_deg > 0:
                cmd = "right"
            else:
                cmd = "left"
            
            self.last_valid_cmd = cmd
            rospy.loginfo(f"Ángulo óptimo: {angle_deg:.1f}° → Comando: {cmd}")
            angle_msg = Float32()
            angle_msg.data = angle_deg
            self.angle_pub.publish(angle_msg)

        if cmd != self.last_cmd:
            self._publish_cmd(cmd)
            self.last_cmd = cmd

    def _publish_cmd(self, cmd):
        """Publica comando de dirección"""
        msg = String()
        msg.data = cmd
        self.cmd_pub.publish(msg)

    def _publish_last_valid_cmd(self):
        """Mantiene el último comando válido"""
        self._publish_cmd(self.last_valid_cmd)

    def _publish_safe_stop(self):
        """Protocolo de emergencia"""
        self._publish_cmd("stop")
        self.last_cmd = "stop"
        self.last_valid_cmd = "stop"

if __name__ == '__main__':
    try:
        node = FusionNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Nodo de fusión detenido")
    except Exception as e:
        rospy.logerr(f"Error fatal: {str(e)}")
