import RPi.GPIO as GPIO
import time

# Configura los pines GPIO para los servos
servo1_pin = 17  # Cambia al pin GPIO que uses
servo2_pin = 27  # Cambia al pin GPIO que uses

# Configuraci�n de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)

# Configura el PWM en el pin del servo
pwm1 = GPIO.PWM(servo1_pin, 50)  # Frecuencia de 50 Hz
pwm2 = GPIO.PWM(servo2_pin, 50)

# Inicia el PWM
pwm1.start(0)
pwm2.start(0)

def set_servo_angle(pwm, angle):
    duty_cycle = angle / 18 + 2  # Conversi�n de �ngulo a ciclo de trabajo
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)

try:
    while True:
        # Mover ambos servos
        set_servo_angle(pwm1, 0)   # Mueve servo 1 a 0�
        set_servo_angle(pwm2, 0)   # Mueve servo 2 a 0�
        time.sleep(1)

        set_servo_angle(pwm1, 90)  # Mueve servo 1 a 90�
        set_servo_angle(pwm2, 90)  # Mueve servo 2 a 90�
        time.sleep(1)

        set_servo_angle(pwm1, 180) # Mueve servo 1 a 180�
        set_servo_angle(pwm2, 180) # Mueve servo 2 a 180�
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
    print("Prueba finalizada.")
