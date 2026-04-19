import Jetson.GPIO as GPIO
import time

# Configuración CORRECTA para Jetson Nano:
IN1 = 17  # GPIO17 (BCM)
IN2 = 18  # GPIO18 (BCM)
ENA = 12  # GPIO12 (PWM0 en BCM) - CORRECTO para PWM hardware

# Configuración inicial CRUCIAL
GPIO.setmode(GPIO.BCM)  # Usamos numeración BCM (Broadcom)
GPIO.setwarnings(True)  # Habilitar advertencias

# Configurar pines
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

def software_pwm(pin, duty_cycle, frequency=1000, duration=5):
    period = 1.0/frequency
    on_time = period * (duty_cycle/100.0)
    off_time = period - on_time
    
    end_time = time.time() + duration
    while time.time() < end_time:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(on_time)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(off_time)

# Uso:
software_pwm(ENA, 80)  # 80% de potencia, 1kHz, 5 segundos