import network
import usocket as socket
import gc
import time
from machine import Pin
from machine import I2C
from ov7670 import OV7670

# Set up Wi-Fi connection
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Connected to WiFi:', wlan.ifconfig())

# Initialize OV7670 camera module
def init_camera():
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
    cam = OV7670(i2c)
    cam.init()
    return cam

# Start streaming video
def stream_video(cam):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 80))
    s.listen(1)
    print('Waiting for connection...')
    while True:
        conn, addr = s.accept()
        print('Connected to:', addr)
        try:
            while True:
                frame = cam.get_frame()
                conn.write(frame)
        except Exception as e:
            print('Error:', e)
            conn.close()
            break
        finally:
            conn.close()
            gc.collect()

# Main function
def main():
    ssid = 'YourWiFiSSID'
    password = 'YourWiFiPassword'
    connect_wifi(ssid, password)
    cam = init_camera()
    stream_video(cam)

if __name__ == '__main__':
    main()