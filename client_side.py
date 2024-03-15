import cv2
import numpy as np
import socket

# ESP32 server IP address and port
SERVER_IP = 'ESP32_IP_ADDRESS'
SERVER_PORT = 80

# Initialize OpenCV window
cv2.namedWindow('Video Stream', cv2.WINDOW_NORMAL)

# Connect to ESP32 server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

while True:
    try:
        # Receive frame from server
        frame_data = client_socket.recv(921600)  # Assuming frame size is 640x480x3 bytes (RGB)
        
        # Reshape received data into numpy array
        frame_array = np.frombuffer(frame_data, dtype=np.uint8)
        frame = frame_array.reshape((480, 640, 3))

        # Display frame
        cv2.imshow('Video Stream', frame)
        
        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except KeyboardInterrupt:
        break

# Clean up
cv2.destroyAllWindows()
client_socket.close()