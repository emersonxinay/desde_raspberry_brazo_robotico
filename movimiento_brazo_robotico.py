import time
from board import SCL, SDA
import busio 
from adafruit_pca9685 import PCA9685
# configurando la el bus I2C y el modulo PCA9685
i2c = busio.I2C(SCL, SDA)
placa = PCA9685(i2c)
placa.frequency = 50 # uso de 50Hz 
# configurar la cantidad de servos que tengo 
servo1 = placa.channels[0]
servo2 = placa.channels[1]
servo3 = placa.channels[2]

# funcion para configurar el servo 
def config_servo(canal, angulo):
    pulso_minimo = 1000
    pulso_maximo = 2000
    pulso_total = pulso_minimo+ (angulo/180.0)* (pulso_maximo-pulso_minimo)
    duty_cycle = int(pulso_total / 1000000 * placa.frequency *0xFFFF)
    canal.duty_cycle = duty_cycle

def menu():
    print("Seleccionar una opcion: ")
    print("1. Mover servo 1")
    print("2. Mover servo 2")
    print("3. Mover servo 3")
    print("4. salir")
    return int(input("Elege una opcion: "))

# dando las indicaciones con manejo de errores
try:
    while True:
        opcion = menu()
        if opcion in [1,2,3]:
            angulo = int(input("ingrese un angulo de 0 a 180: "))
            if 0 <= angulo <= 180:
                if opcion == 1:
                    config_servo(servo1, angulo)
                elif opcion == 2:
                    config_servo(servo2, angulo)
                elif opcion == 3:
                    config_servo(servo3, angulo)
                
                print(f"servo {opcion} se movio a un angulo de {angulo} ")
            else:
                print("Error: angulo fuera de rango")
        elif opcion == 4:
            print("saliendo ...")
            break
        else:
            print("Opcion no valida, intente nuevamente")
except KeyboardInterrupt:
    print("INterrupcion del programa")

finally:
    # apagando todos los servos
    servo1.duty_cycle = 0
    servo2.duty_cycle = 0
    servo3.duty_cycle = 0
    print("Servos apagados")
