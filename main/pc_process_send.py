# ------- Import Libraries ---------------------------------------------------------------------------------------------------
import torch
import pickle
import socket
import struct
from utils_main.utils_PC import*

# ------- Conection To Raspi ---------------------------------------------------------------------------------------------------

# Listen
PORT_GET = 8485
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('',PORT_GET))
s.listen(10)
print('Socket now listening')
conn,addr = s.accept()
data = b""
payload_size = struct.calcsize(">L")

# Client
PORT_SEND = 12345
raspi_ip = '192.168.19.98'
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((raspi_ip, PORT_SEND))
connection = client_socket.makefile('wb')

# ------- Process Structure Bult --------------------------------------------------------------------------
PC = PCProcess() # Create PCProcess

# Computer Vision
PC.model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best.pt', source='github') # Load YOLOv5 model
PC.tracker = dlib.correlation_tracker() # Tracker dlib

# Servo
velocity = 10 # Camera velocity
PC.create_servo(17,18,velocity) # Create servo

# Control variables
searching = True
frame_count = 0
reinit_interval  = 200


# ------- Get Data  ---------------------------------------------------------------------------------------------------
while True:

    # Receiving data
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes") # Decoding frame
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    # Process frame
    PC.process_frame(frame)

    # Detacting drone
    if PC.serching:
        PC.detect() # Try to detect drone
        searching = False # Stop seacrh for drone

    # Track drone
    else:
        PC.track() # Track drone detected
        frame_count += 1 # Update frame cont

        # Send data
        data = f"{PC.servo_x.angle}, {PC.servo_y.angle}".encode()
        client_socket.sendall(data)

    # Check counter
    if frame_count == reinit_interval:
        searching = True # Resetart searching
        frame_count = 0 # Reset frame cont



    # displaying the frame
    cv2.imshow('frame',frame)
    cv2.waitKey(1)

    # Wait for a keyboard event to brake
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
cv2.destroyAllWindows()