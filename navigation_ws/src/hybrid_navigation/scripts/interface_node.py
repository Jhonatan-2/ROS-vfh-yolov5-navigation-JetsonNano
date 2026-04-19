#!/usr/bin/env python3
import rospy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, Wedge
from std_msgs.msg import Float32, Float32MultiArray

class NavigationRadar:
    def __init__(self):
        rospy.init_node('navigation_radar_interface')
        self.safety_distance = 1.0
        self.fov_deg = 120  # Campo visual total (±60°)
        
        # Inicialización flexible
        self.danger_map = None
        self.best_angle_deg = 0.0
        self.num_sectors = None
        
        # Subscripciones
        rospy.Subscriber('/fusion/danger_map', Float32MultiArray, self.map_callback)
        rospy.Subscriber('/cmd_angle', Float32, self.angle_callback)

        # Configuración del radar
        self.setup_radar()
        self.running = True
        rospy.loginfo(" Radar de peligro inicializado - Visualización mejorada")

    def setup_radar(self):
        """Configura la visualización avanzada del radar"""
        plt.ion()  # Modo interactivo
        self.fig, self.ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': 'polar'})
        self.fig.canvas.manager.set_window_title('Sistema de Navegación - Mapa de Peligro')
        self.fig.canvas.mpl_connect('close_event', self.handle_close)
        
        # Configuración polar
        self.ax.set_theta_zero_location('N')
        self.ax.set_theta_direction(-1)
        self.ax.set_title("Mapa de Densidad de Peligro", pad=25, fontsize=16, fontweight='bold')
        
        # Configuración de límites
        self.max_radius = self.safety_distance * 1.8
        self.ax.set_ylim(0, self.max_radius)
        self.ax.set_thetamin(-self.fov_deg/2)
        self.ax.set_thetamax(self.fov_deg/2)
        
        # Crear colormap personalizado (verde -> amarillo -> rojo)
        colors = ["#2ECC71", "#F1C40F", "#E74C3C", "#7D3C98"]
        self.danger_cmap = LinearSegmentedColormap.from_list("danger_map", colors)
        
        # Elementos decorativos
        self.safe_zone = Circle((0, 0), self.safety_distance, color='#ABEBC6', alpha=0.25, zorder=1)
        self.ax.add_patch(self.safe_zone)
        
        # Líneas de referencia
        self.ax.plot(np.radians([0, 0]), [0, self.max_radius], 'k-', alpha=0.4, linewidth=1)  # Línea central
        self.ax.plot(np.radians([-self.fov_deg/2, self.fov_deg/2]), [self.safety_distance]*2, 'g--', alpha=0.7)  # Distancia segura
        
        # Flecha de dirección (inicialmente invisible)
        self.direction_arrow = self.ax.arrow(0, 0, 0, 0, 
                                            width=0.08, 
                                            color='#1F618D', 
                                            alpha=0.9, 
                                            length_includes_head=True,
                                            zorder=10)
        self.direction_arrow.set_visible(False)
        
        # Texto informativo
        self.info_text = self.ax.text(0.05, 0.95, "Inicializando...", 
                                     transform=self.ax.transAxes, 
                                     fontsize=10,
                                     bbox=dict(facecolor='white', alpha=0.7))
        
        # Cuña de peligro (placeholder)
        self.danger_wedge = None
        
        # Rejilla y etiquetas
        self.ax.grid(True, alpha=0.4, linestyle='--')
        self.ax.set_rlabel_position(45)  # Posición de las etiquetas radiales
        
        # Leyenda de colores
        self.cbar = self.fig.colorbar(plt.cm.ScalarMappable(cmap=self.danger_cmap), 
                                     ax=self.ax, 
                                     pad=0.1,
                                     label='Nivel de peligro')
        self.cbar.set_ticks([0, 0.5, 1.0])
        self.cbar.set_ticklabels(['Bajo', 'Medio', 'Alto'])
        
        plt.tight_layout()

    def map_callback(self, msg):
        """Actualiza el mapa de peligro con manejo dinámico de tamaño"""
        self.danger_map = np.array(msg.data)
        self.num_sectors = len(self.danger_map)
        rospy.logdebug(f"Mapa actualizado con {self.num_sectors} sectores")

    def angle_callback(self, msg):
        self.best_angle_deg = msg.data

    def handle_close(self, event):
        rospy.signal_shutdown("Interfaz cerrada por el usuario")
        self.running = False

    def update_radar(self):
        """Actualiza la visualización con mapa de calor polar"""
        if not self.running or self.danger_map is None or self.num_sectors is None:
            return
            
        try:
            # Limpiar elementos anteriores
            if self.danger_wedge:
                self.danger_wedge.remove()
            
            # Calcular ángulos y valores de peligro
            sector_angles_deg = np.linspace(-self.fov_deg/2, self.fov_deg/2, self.num_sectors)
            sector_angles_rad = np.radians(sector_angles_deg)
            
            # Normalizar peligro (0-1)
            danger_normalized = self.danger_map / np.max(self.danger_map)
            
            # Crear mapa de calor polar
            for i in range(self.num_sectors):
                start_angle = sector_angles_rad[i]
                end_angle = sector_angles_rad[i+1] if i < self.num_sectors-1 else sector_angles_rad[0]
                danger_value = danger_normalized[i]
                
                # Crear cuña para este sector
                wedge = Wedge(
                    (0, 0), 
                    self.max_radius * 0.95,  # Radio de visualización
                    np.degrees(start_angle), 
                    np.degrees(end_angle),
                    width=self.max_radius * 0.95 - self.safety_distance * 0.2,
                    color=self.danger_cmap(danger_value),
                    alpha=0.7
                )
                self.ax.add_patch(wedge)
            
            # Actualizar zona segura (si cambia el tamaño)
            self.safe_zone.set_radius(self.safety_distance)
            
            # Actualizar flecha de dirección
            if -self.fov_deg/2 <= self.best_angle_deg <= self.fov_deg/2:
                arrow_length = self.safety_distance * 0.8
                self.direction_arrow.set_data(
                    x=np.radians(self.best_angle_deg),
                    y=0,
                    dx=0,
                    dy=arrow_length
                )
                self.direction_arrow.set_visible(True)
                direction_text = f"Dirección segura: {self.best_angle_deg:.1f}°"
            else:
                self.direction_arrow.set_visible(False)
                direction_text = "¡Buscar dirección segura!"
                rospy.logdebug_throttle(10, f"Ángulo óptimo fuera de FOV: {self.best_angle_deg:.1f}°")
            
            # Actualizar texto informativo
            max_danger = np.max(self.danger_map)
            min_danger = np.min(self.danger_map)
            danger_info = (f"Peligro: MAX {max_danger:.2f}m | MIN {min_danger:.2f}m\n"
                          f"Dirección: {self.best_angle_deg:.1f}°\n"
                          f"Sectores: {self.num_sectors}")
            self.info_text.set_text(danger_info)
            
            # Actualizar colores de la barra de peligro
            self.cbar.update_normal(plt.cm.ScalarMappable(cmap=self.danger_cmap))
            
            # Redibujar
            self.fig.canvas.draw_idle()
            self.fig.canvas.flush_events()
            
        except Exception as e:
            rospy.logerr(f"Error al actualizar radar: {str(e)}")
            rospy.logerr(f"Formas: danger_map={self.danger_map.shape if hasattr(self.danger_map, 'shape') else 'None'}, " +
                         f"sectores={self.num_sectors}")

    def run(self):
        rospy.loginfo(" Radar operativo. Esperando datos...")
        rate = rospy.Rate(10)  # 10 Hz (óptimo para visualización)
        while not rospy.is_shutdown() and self.running:
            self.update_radar()
            rate.sleep()

if __name__ == '__main__':
    try:
        radar = NavigationRadar()
        radar.run()
    except rospy.ROSInterruptException:
        plt.close('all')
        rospy.loginfo("Nodo finalizado")
