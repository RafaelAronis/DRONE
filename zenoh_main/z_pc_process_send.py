# ------- Import Libraries ---------------------------------------------------------------------------------------------------
import cv2
import json
import zenoh
import torch
import socket
import numpy as np
from utils_main.utils_PC import*

# ------- Socket Client Raspi Conection---------------------------------------------------------------------------------------------------
PORT_SEND = 12345
raspi_ip = '192.168.16.159'
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((raspi_ip, PORT_SEND))
connection = client_socket.makefile('wb')

# ------- Zenoh SUB Conection ---------------------------------------------------------------------------------------------------

# Parameters
IP = '0.0.0.0'
PORT = '7447'
mode = 'peer' # Zenoh session mode ('peer' or 'client')
connect = [f"tcp/{IP}:{PORT}"] # Zenoh endpoints to listen on
key = 'demo/zcam' # Key expression

# Zenoh config
conf = zenoh.Config()
conf.insert_json5(zenoh.config.MODE_KEY, json.dumps(mode))
conf.insert_json5(zenoh.config.CONNECT_KEY, json.dumps(connect))

# Callback -------------------------------------------------------------------------------------------------------
cams = {}
def frames_listener(sample):
    npImage = np.frombuffer(bytes(sample.value.payload), dtype=np.uint8)
    matImage = cv2.imdecode(npImage, 1)

    cams[sample.key_expr] = matImage


zenoh.init_logger()
z = zenoh.open(conf)
sub = z.declare_subscriber(key, frames_listener)


# ------- Process Structure Bult --------------------------------------------------------------------------
PC = PCProcess() # Create PCProcess

# Computer Vision
PC.model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best.pt', source='github') # Load YOLOv5 model
PC.tracker = dlib.correlation_tracker() # Tracker dlib

# Check for CUDA
if torch.cuda.is_available():
    device = torch.device("cuda")
    PC.model.to(device).half()

# Servo
velocity = 10 # Camera velocity
PC.create_servo(17,18,velocity) # Create servo

# Control variables
frame_count = 0
reinit_interval  = 200


# ------- Get Data  ---------------------------------------------------------------------------------------------------
while True:
    for cam in list(cams):
        frame = cams[cam]

        # Process frame
        PC.process_frame(frame)

        # Detacting drone
        if PC.searching:
            PC.detect() # Try to detect drone

        # Track drone
        else:
            PC.track() # Track drone detected
            frame_count += 1 # Update frame cont

            # Send data
            data_send = f"{PC.servo_x.angle}, {PC.servo_y.angle}".encode()
            client_socket.sendall(data_send)

        # Check counter
        if frame_count == reinit_interval:
            PC.searching = True # Resetart searching
            frame_count = 0 # Reset frame cont

        # displaying the frame
        cv2.imshow(str(cam), frame)

    # Wait for a keyboard event to brake
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
cv2.destroyAllWindows()
sub.undeclare()
z.close()