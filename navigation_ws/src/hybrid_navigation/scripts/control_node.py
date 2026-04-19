#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Joy
import Jetson.GPIO as GPIO
import time

class MotorController:
    def __init__(self):
        # Setup ROS node
        rospy.init_node('xbox_diff_drive_digital')
        
        # Pin mapping - solo usamos pines de dirección (IN1, IN2)
        self.LEFT_IN1 = 17
        self.LEFT_IN2 = 18

        self.RIGHT_IN1 = 27
        self.RIGHT_IN2 = 22

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.LEFT_IN1, self.LEFT_IN2, self.RIGHT_IN1, self.RIGHT_IN2], GPIO.OUT)
        
        # Apagar todos los motores inicialmente
        GPIO.output(self.LEFT_IN1, GPIO.LOW)
        GPIO.output(self.LEFT_IN2, GPIO.LOW)
        GPIO.output(self.RIGHT_IN1, GPIO.LOW)
        GPIO.output(self.RIGHT_IN2, GPIO.LOW)

        # Variables máximas
        self.max_linear_speed = 0.5    # m/s
        self.max_angular_speed = 1.0   # rad/s
        self.deadzone_threshold = 0.2  # Zona muerta del joystick

        # Suscribirse al joystick
        rospy.Subscriber("/joy", Joy, self.joy_callback)

        rospy.loginfo("Nodo de control digital de motores iniciado")

    def joy_callback(self, joy_msg):
        # Botones principales (Xbox: A=0, B=1, X=2, Y=3)
        # Ejes: [0]=Horizontal izquierdo, [1]=Vertical izquierdo
        
        # Usar eje vertical izquierdo para adelante/atrás
        linear_axis = joy_msg.axes[1]   # eje vertical izquierdo
        
        # Usar eje horizontal izquierdo para giro
        angular_axis = joy_msg.axes[0]  # eje horizontal izquierdo
        
        # Botón de parada de emergencia (START o BACK)
        if joy_msg.buttons[7] or joy_msg.buttons[6]:  # START=7, BACK=6 en Xbox
            self.set_motor_commands("STOP", "STOP")
            rospy.logwarn("¡PARADA DE EMERGENCIA ACTIVADA!")
            return

        # Aplicar zona muerta
        if abs(linear_axis) < self.deadzone_threshold:
            linear_axis = 0.0
        if abs(angular_axis) < self.deadzone_threshold:
            angular_axis = 0.0

        # Convertir a comandos digitales
        left_cmd, right_cmd = self.calculate_motor_commands(linear_axis, angular_axis)
        
        # Aplicar comandos a los motores
        self.set_motor_commands(left_cmd, right_cmd)

    def calculate_motor_commands(self, linear, angular):
        """Calcula comandos digitales para los motores basado en entradas analógicas"""
        # Detener por defecto
        left_cmd = "STOP"
        right_cmd = "STOP"
        
        # Movimiento puramente lineal
        if abs(angular) < 0.1 and abs(linear) > 0.1:
            if linear > 0:
                left_cmd = "FORWARD"
                right_cmd = "FORWARD"
            else:
                left_cmd = "BACKWARD"
                right_cmd = "BACKWARD"
        
        # Giro en el lugar
        elif abs(linear) < 0.1 and abs(angular) > 0.1:
            if angular > 0:
                left_cmd = "FORWARD"
                right_cmd = "BACKWARD"
            else:
                left_cmd = "BACKWARD"
                right_cmd = "FORWARD"
        
        # Movimiento combinado (lineal + angular)
        elif abs(linear) > 0.1 and abs(angular) > 0.1:
            if linear > 0:
                if angular > 0:  # Avanzar y girar a la derecha
                    left_cmd = "FORWARD"
                    right_cmd = "STOP"
                else:  # Avanzar y girar a la izquierda
                    left_cmd = "STOP"
                    right_cmd = "FORWARD"
            else:
                if angular > 0:  # Retroceder y girar a la derecha
                    left_cmd = "BACKWARD"
                    right_cmd = "STOP"
                else:  # Retroceder y girar a la izquierda
                    left_cmd = "STOP"
                    right_cmd = "BACKWARD"
        
        return left_cmd, right_cmd

    def set_motor_commands(self, left_cmd, right_cmd):
        """Aplica comandos digitales a los motores"""
        # Motor izquierdo
        if left_cmd == "FORWARD":
            GPIO.output(self.LEFT_IN1, GPIO.HIGH)
            GPIO.output(self.LEFT_IN2, GPIO.LOW)
        elif left_cmd == "BACKWARD":
            GPIO.output(self.LEFT_IN1, GPIO.LOW)
            GPIO.output(self.LEFT_IN2, GPIO.HIGH)
        else:  # STOP
            GPIO.output(self.LEFT_IN1, GPIO.LOW)
            GPIO.output(self.LEFT_IN2, GPIO.LOW)
        
        # Motor derecho
        if right_cmd == "FORWARD":
            GPIO.output(self.RIGHT_IN1, GPIO.HIGH)
            GPIO.output(self.RIGHT_IN2, GPIO.LOW)
        elif right_cmd == "BACKWARD":
            GPIO.output(self.RIGHT_IN1, GPIO.LOW)
            GPIO.output(self.RIGHT_IN2, GPIO.HIGH)
        else:  # STOP
            GPIO.output(self.RIGHT_IN1, GPIO.LOW)
            GPIO.output(self.RIGHT_IN2, GPIO.LOW)

    def run(self):
        rospy.spin()

    def cleanup(self):
        # Apagar todos los motores antes de salir
        GPIO.output(self.LEFT_IN1, GPIO.LOW)
        GPIO.output(self.LEFT_IN2, GPIO.LOW)
        GPIO.output(self.RIGHT_IN1, GPIO.LOW)
        GPIO.output(self.RIGHT_IN2, GPIO.LOW)
        GPIO.cleanup()

if __name__ == '__main__':
    controller = None
    try:
        controller = MotorController()
        controller.run()
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        if controller is not None:
            controller.cleanup()