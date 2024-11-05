import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

# Configura el bus I2C y el m�dulo PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Frecuencia de 50Hz para los servos

# Configuraci�n de los canales para los dos servos
servo1 = pca.channels[0]  # Servo 1 en el canal 0
servo2 = pca.channels[1]  # Servo 2 en el canal 1

def set_servo_angle(channel, angle):
    pulse_min = 1000  # Ajusta seg�n la especificaci�n de tu servo
    pulse_max = 2000
    pulse_width = pulse_min + (angle / 180.0) * (pulse_max - pulse_min)
    duty_cycle = int(pulse_width / 1000000 * pca.frequency * 0xFFFF)
    channel.duty_cycle = duty_cycle

try:
    while True:
        # Mover ambos servos a 0�, 90� y 180� simult�neamente
        set_servo_angle(servo1, 0)
        set_servo_angle(servo2, 0)
        time.sleep(1.5)

        set_servo_angle(servo1, 90)
        set_servo_angle(servo2, 90)
        time.sleep(1.5)

        set_servo_angle(servo1, 180)
        set_servo_angle(servo2, 180)
        time.sleep(1.5)

except KeyboardInterrupt:
    # Apaga ambos servos cuando el programa finalice
    servo1.duty_cycle = 0
    servo2.duty_cycle = 0
    print("Programa finalizado.")
