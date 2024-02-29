# ------- Import --------------------------------------------------------------------------
import cv2
import torch
from PIL import Image

# ------- RUN --------------------------------------------------------------------------
video_capture = cv2.VideoCapture(0) #  Camera video capture
model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best.pt', source='github') # Load YOLOv5 model

# Check for CUDA
if torch.cuda.is_available():
    device = torch.device("cuda")
    model.to(device).half()

while True:

    # Frame preparation
    ret, frame = video_capture.read() # Reads camera's frame
    img = Image.fromarray(frame[...,::-1]) # Convert the frame to a format that YOLOv5 can process

    # Run inference on the frame (change size = change FPS)
    results = model(img, size=640)

    # Process the results and draw bounding boxes on the frame
    for result in results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = result.tolist()
        if conf > 0.5:

            # Draw the bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

            # Get Center
            cx,cy = (x1+x2)/2,(y1+y2)/2

            # Display the confidence score above the box
            text_conf = "{:.2f}%".format(conf * 100)
            cv2.putText(frame, text_conf, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Display the bounding box coordinates below the box
            text_coords = "({}, {})".format(int((x1 + x2) / 2), int(y2))
            cv2.putText(frame, text_coords, (int(x1), int(y2) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Shows the frame on the screen
    cv2.imshow('frame', frame)

    # Wait for a keyboard event to brake
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
video_capture.release()
cv2.destroyAllWindows()
