from flask import Flask, render_template, request
import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

app = Flask(__name__)

# Configura el bus I2C y el m�dulo PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Frecuencia de 50Hz para los servos

# Configuraci�n de los canales para los dos servos
servo1 = pca.channels[0]  # Servo 1 en el canal 0
servo2 = pca.channels[1]  # Servo 2 en el canal 1

def set_servo_angle(angle):
    pulse_min = 1000  # Ajusta seg�n la especificaci�n de tu servo
    pulse_max = 2000
    pulse_width = pulse_min + (angle / 180.0) * (pulse_max - pulse_min)
    duty_cycle = int(pulse_width / 1000000 * pca.frequency * 0xFFFF)
    servo1.duty_cycle = duty_cycle
    servo2.duty_cycle = duty_cycle

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        angle = request.form.get('angle', type=int)
        if angle is not None and 0 <= angle <= 180:
            set_servo_angle(angle)
            return f'Servos movidos a {angle} grados'
        else:
            return '�ngulo inv�lido. Debe estar entre 0 y 180.'
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
