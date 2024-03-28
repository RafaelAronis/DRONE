# ------- Import Libraries ---------------------------------------------------------------------------------------------------
import cv2
import json
import zenoh
import torch
import socket
import argparse
import numpy as np
from utils_main.utils_PC import*

# ------- Parser ---------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(
    prog='z_pc_process_send',
    description='zenoh video capture example')
parser.add_argument('-l', '--connect', type=str, default='tcp/0.0.0.0:7447',
                    help='zenoh endpoints to listen on (raspi IP and port).')
parser.add_argument('-s', '--servo_ip', type=str, default=parser.parse_args().connect.split('/')[1].split(':')[0],
                    help='zenoh endpoints to listen on (raspi IP and port).')
parser.add_argument('-p', '--port_send', type=int, default=12345,
                    help='scket send port')
parser.add_argument('-k', '--key', type=str, default='demo/zcam',
                    help='key expression')
parser.add_argument('-m', '--model_path', type=str, default='models/best.pt',
                    help='model used path')

args = parser.parse_args()

# ------- Socket Servo Conection---------------------------------------------------------------------------------------------------
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f'[INFO] Socket conection at {args.servo_ip}:{args.port_send}...')
client_socket.connect((args.servo_ip, args.port_send))
connection = client_socket.makefile('wb')

# ------- Zenoh SUB Conection ---------------------------------------------------------------------------------------------------
cams = {}
def frames_listener(sample):
    npImage = np.frombuffer(bytes(sample.value.payload), dtype=np.uint8)
    matImage = cv2.imdecode(npImage, 1)
    cams[sample.key_expr] = matImage
conf = zenoh.Config()
conf.insert_json5(zenoh.config.MODE_KEY, json.dumps('peer'))
conf.insert_json5(zenoh.config.CONNECT_KEY, json.dumps([args.connect]))
print(f'[INFO] Open zenoh session at {args.connect} ...')
zenoh.init_logger()
z = zenoh.open(conf)
sub = z.declare_subscriber(args.key, frames_listener)

# ------- Process Structure Bult --------------------------------------------------------------------------
PC = PCProcess() # Create PCProcess

# Computer Vision
print(f'[INFO] Loading Model from {args.model_path} ...')
PC.model = torch.hub.load('ultralytics/yolov5', 'custom', path=args.model_path, source='github') # Load YOLOv5 model
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

print(f'[INFO] All done ...')


# ------- Get Data  ---------------------------------------------------------------------------------------------------
try:
    while True:
        for cam in list(cams):
            frame = cams[cam]

            # Process frame
            PC.process_frame(frame)

            # Run model
            if PC.searching: # Detacting drone
                PC.detect() # Try to detect drone
            else: # Track drone
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
except:
    pass

# Release the resources
print(f'[INFO] Quiting ...')
cv2.destroyAllWindows()
sub.undeclare()
z.close()