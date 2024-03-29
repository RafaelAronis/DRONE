# ------- Import Libraries ---------------------------------------------------------------------------------------------------
import cv2
import json
import zenoh
import torch
import argparse
import numpy as np
from utils_main.utils_PC import*

# ------- Parser ---------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(
    prog='z_pc_process_send',
    description='zenoh video capture example')
parser.add_argument('-s', '--sub', type=str, default='tcp/0.0.0.0:7447',
                    help='zenoh endpoints to listen on (raspi IP and port).')
parser.add_argument('-p', '--pub', type=str, default='tcp/0.0.0.0:7441',
                    help='zenoh endpoints to listen on (raspi IP and port).')
parser.add_argument('-ks', '--key_sub', type=str, default='drone/frame',
                    help='key sub expression')
parser.add_argument('-kp', '--key_pub', type=str, default='drone/servo',
                    help='key pub expression')
parser.add_argument('-m', '--model_path', type=str, default='models/best.pt',
                    help='model used path')
args = parser.parse_args()


# ------- Zenoh SUB Conection ---------------------------------------------------------------------------------------------------

# Zenoh SUB
cams = {}
def frames_listener(sample):
    npImage = np.frombuffer(bytes(sample.value.payload), dtype=np.uint8)
    matImage = cv2.imdecode(npImage, 1)
    cams[sample.key_expr] = matImage
conf = zenoh.Config()
conf.insert_json5(zenoh.config.MODE_KEY, json.dumps('peer'))
conf.insert_json5(zenoh.config.CONNECT_KEY, json.dumps([args.sub]))
print(f'[INFO] Open zenoh session at {args.sub} as SUB...')
zenoh.init_logger()
z = zenoh.open(conf)
sub = z.declare_subscriber(args.key_sub, frames_listener)

# Zenoh PUB
conf = zenoh.Config()
conf.insert_json5(zenoh.config.MODE_KEY, json.dumps('peer'))
conf.insert_json5(zenoh.config.LISTEN_KEY, json.dumps([args.pub]))
print(f'[INFO] Open zenoh session at {args.pub} as PUB...')
zenoh.init_logger()
z = zenoh.open(conf)
session = zenoh.open(conf)
pub = session.declare_publisher(args.key_pub)

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
                pub.put(f"{PC.servo_x.angle}, {PC.servo_y.angle}") # PUB object coordnates
            if frame_count == reinit_interval: # Check counter
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