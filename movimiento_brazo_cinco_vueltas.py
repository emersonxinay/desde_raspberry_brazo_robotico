import time
from board import SCL, SDA
import busio 
from adafruit_pca9685 import PCA9685

# Configurando el bus I2C y el m�dulo PCA9685
i2c = busio.I2C(SCL, SDA)
placa = PCA9685(i2c)
placa.frequency = 50  # Frecuencia de 50Hz para servos

# Configuraci�n de los canales para los tres servos
servo1 = placa.channels[0]
servo2 = placa.channels[1]
servo3 = placa.channels[2]

# Funci�n para configurar el �ngulo del servo
def config_servo(canal, angulo):
    pulso_minimo = 1000
    pulso_maximo = 2000
    pulso_total = pulso_minimo + (angulo / 180.0) * (pulso_maximo - pulso_minimo)
    duty_cycle = int(pulso_total / 1000000 * placa.frequency * 0xFFFF)
    canal.duty_cycle = duty_cycle

# Secuencia de movimiento para los servos
def secuencia_movimiento():
    config_servo(servo1, 0)
    config_servo(servo2, 90)
    config_servo(servo3, 180)
    time.sleep(1)
    
    config_servo(servo1, 180)
    config_servo(servo2, 0)
    config_servo(servo3, 90)
    time.sleep(1)
    
    config_servo(servo1, 90)
    config_servo(servo2, 180)
    config_servo(servo3, 0)
    time.sleep(1)

# Funci�n principal para controlar el flujo
def main():
    print("Iniciando secuencia de movimiento de servos... (Ctrl+C para salir)")
    
    pausa = False  # Variable de control para pausar o continuar el "baile"
    vueltas = 0    # Contador de vueltas
    
    try:
        while True:
            if not pausa:
                for _ in range(5):  # Realizar 5 vueltas de secuencia de movimiento
                    secuencia_movimiento()
                vueltas += 1
                print(f"{vueltas} ciclos de 5 vueltas completados.")
            else:
                print("Movimiento pausado. Presiona 'Enter' para continuar...")
                input()  # Espera a que el usuario presione Enter para reanudar
                pausa = False
            
            # Detener la secuencia de movimiento al recibir la entrada del usuario
            opcion = input("Escribe 'stop' para pausar, 'go' para continuar: ").strip().lower()
            if opcion == 'stop':
                pausa = True
            elif opcion == 'go':
                pausa = False
    
    except KeyboardInterrupt:
        print("\nInterrupci�n del programa.")

    finally:
        # Apaga todos los servos al salir del programa
        servo1.duty_cycle = 0
        servo2.duty_cycle = 0
        servo3.duty_cycle = 0
        print("Servos apagados.")

# Ejecutar el programa
main()
