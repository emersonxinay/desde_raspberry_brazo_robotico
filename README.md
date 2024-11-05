# Conexión a Raspberry Pi utilizando VNC Viewer

Esta guía proporciona los pasos necesarios para configurar y conectar tu Raspberry Pi a través de VNC Viewer desde un sistema Windows, sin necesidad de teclado, pantalla ni ratón.

## 1. Preparar la Tarjeta SD

### 1.1. Grabar el Sistema Operativo

1. **Descargar Raspberry Pi Imager:**

   - Visita [Raspberry Pi Imager](https://www.raspberrypi.com/software/) y descarga la aplicación para tu sistema operativo.

2. **Grabar el Sistema Operativo:**

   - Inserta la tarjeta SD en tu computadora.
   - Abre Raspberry Pi Imager.
   - Selecciona el sistema operativo que deseas instalar (por ejemplo, Raspberry Pi OS).
   - Antes de grabar, presiona `Ctrl + Shift + X` para abrir la configuración de opciones avanzadas.

3. **Configurar Opciones Avanzadas:**

   - En la ventana de configuración, puedes:
     - **Establecer el nombre de host:** Cambia el nombre de tu Raspberry Pi (ejemplo: `raspberry1`).
     - **Configurar la red Wi-Fi:** Activa la opción de "Configure Wi-Fi" y proporciona el SSID y la contraseña de tu red Wi-Fi.
     - **Habilitar SSH:** Marca la opción para habilitar SSH.
   - Haz clic en "Guardar" para aplicar los cambios.

4. **Grabar la Imagen:**

   - Selecciona la tarjeta SD como destino y haz clic en "Escribir" para grabar el sistema operativo y aplicar la configuración.

5. **Habilitar SSH:**

   - Después de grabar el sistema operativo, inserta la tarjeta SD en tu computadora.
   - En la partición de arranque (boot), crea un archivo vacío llamado `ssh` (sin extensión). Esto habilitará el acceso SSH automáticamente al arrancar la Raspberry Pi.

6. **Configurar Wi-Fi:**

   - En la misma partición de arranque, crea un archivo llamado `wpa_supplicant.conf` con el siguiente contenido, reemplazando `TU_SSID` y `TU_CONTRASEÑA`:

   ```plaintext
   country=ES
   ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
   update_config=1

   network={
       ssid="TU_SSID"
       psk="TU_CONTRASEÑA"
       key_mgmt=WPA-PSK
   }
   ```

# 2. dejar listo en windows para Descargar e Instalar VNC Viewer

1. Visita el [sitio web de VNC Viewer](https://www.realvnc.com/en/connect/download/viewer/).
2. Descarga la versión para Windows e instálala en tu computadora.

#3 . verificar que en la misma red este conectado raspberry
y si ya aparece:

Conectarse a la Raspberry Pi usando CMD en Windows

1. **Abrir CMD:**

   - Presiona `Win + R`, escribe `cmd` y presiona `Enter` para abrir la línea de comandos de Windows.

2. **Conectar a la Raspberry Pi a través de SSH:**
   - En la línea de comandos, escribe el siguiente comando, reemplazando `direccion_ip_de_tu_raspberry` con la dirección IP que encontraste anteriormente:
   ```bash
   ssh pi@direccion_ip_de_tu_raspberry
   ```

## Prueba de Servos con PCA9685
```bash
pip install adafruit-circuitpython-pca9685
``` 
```bash
pip install adafruit-circuitpython-board
```
```bash
pip install adafruit-circuitpython-busio

```
## habilitar I2C para controlar servos 
```bash
sudo raspi-config
``` 
- Navega a Interfacing Options.
- Selecciona I2C y aseg�rate de habilitarlo.
- Sal del men� y reinicia tu Raspberry Pi.



Para instalar los modulos 
```bash
   pip install -r requirements.txt
```
