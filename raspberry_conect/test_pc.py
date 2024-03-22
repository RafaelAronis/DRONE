# ------- Import --------------------------------------------------------------------------
import cv2
import dlib
import torch
import socket
from PIL import Image
from utils2 import*

# ------- Conection ---------------------------------------------------------------------------------------------------
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.19.98', 12345))
connection = client_socket.makefile('wb')

# ------- Track --------------------------------------------------------------------------
video_capture = cv2.VideoCapture(0) #  Camera video capture
model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best.pt', source='github') # Load YOLOv5 model
tracker = dlib.correlation_tracker() # Tracker dlib

# Check for CUDA
if torch.cuda.is_available():
    device = torch.device("cuda")
    model.to(device).half()

# Control variables
detect = True
frame_count = 0
reinit_interval  = 200

# Create camera aime tracker
cam_tracker = CamAimTracker(video_capture)
cam_tracker.v = 10 # Camera velocity
cam_tracker.create_servo(17,18) # Create servo

while True:

    # Frame preparation
    ret, frame = video_capture.read() # Reads camera's frame
    img = Image.fromarray(frame[...,::-1]) # Convert the frame to a format that YOLOv5 can process

    # Detect drone
    if detect:

        # Run inference on the frame (change size = change FPS)
        results = model(img, size=640)

        # Process the results and draw bounding boxes on the frame
        for result in results.xyxy[0]:
            x1, y1, x2, y2, conf, cls = result.tolist()
            if conf > 0.5: # Detection
                x1, y1, x2, y2 = map(int, result[:4]) # Convert to intergers
                bbox = (x1, y1, x2, y2) # Creat boc
                tracker.start_track(frame, dlib.rectangle(*bbox)) # Create checker

                # Draw the bounding box
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

                # Stop detection
                detect = False

                # Move servo motors
                cam_tracker.x,cam_tracker.y = (x1+x2)/2,(y1+y2)/2
                cam_tracker.adjust()
                # data = f"{cam_tracker.servo_x.angle}, {cam_tracker.servo_y.angle}\n".encode()
                # client_socket.sendall(data)


    # Track drone
    else:

        # Tracking
        tracker.update(frame)
        tracked_bbox = tracker.get_position()

        # Draw the bounding box
        bbox = int(tracked_bbox.left()), int(tracked_bbox.top()), int(tracked_bbox.width()), int(tracked_bbox.height())
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)

        # Update frame cont
        frame_count += 1
        cam_tracker.x, cam_tracker.y = bbox[0]+bbox[2]/2, bbox[1]+bbox[3]/2
        cam_tracker.adjust()
        data = f"{cam_tracker.servo_x.angle}, {cam_tracker.servo_y.angle}".encode()
        print(data.decode())
        client_socket.sendall(data)

    # Check counter
    if frame_count == reinit_interval:
        detect = True
        frame_count = 0

    # Shows the frame on the screen
    cv2.imshow('frame', frame)

    # Wait for a keyboard event to brake
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Libera os recursos
video_capture.release()
cv2.destroyAllWindows()
