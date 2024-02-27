# ------- Import ---------------------------------------------------------------------------------------------------
import os
import cv2
import torch
import pyautogui
import numpy as np
from PIL import Image

import pygetwindow as gw

from pynput.mouse import Button, Controller

# ------- Functions -----------------------------------------------------------------------------------------------
def get_chrome_screenshot():
    try:
        chrome_window = [window for window in gw.getAllTitles() if 'Google Chrome' in window][0]
        window = gw.getWindowsWithTitle(chrome_window)[0]
        x, y, width, height = window.left, window.top, window.width, window.height
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    except IndexError:
        print("Janela do Google Chrome não encontrada.")
        return None

# ------- RUN -----------------------------------------------------------------------------------------------------
model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best.pt', source='github') # Load YOLO model
window_title  = "ChatGPT - Google Chrome" #  Window capture title
classes = ['Drone'] # Classes to detect
mouse = Controller()
follow_mouse = False


while True:

    # Frame preparation
    frame = get_chrome_screenshot()
    img = Image.fromarray(frame[...,::-1]) # Convert the frame to a format that YOLOv5 can process

    # Run inference on the frame (change size = change FPS)
    results = model(img, size=640)

    # Process the results and draw bounding boxes on the frame
    for result in results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = result.tolist()
        if conf > 0.5 and classes[int(cls)] in classes:

            # Follow mouse
            if follow_mouse:
                mouse.position = ((x1+x2)/2,(y1+y2)/2)

            # Draw the bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

            # Display the confidence score above the box
            text_conf = "{:.2f}%".format(conf * 100)
            cv2.putText(frame, text_conf, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Display the bounding box coordinates below the box
            text_coords = "({}, {})".format(int((x1 + x2) / 2), int(y2))
            cv2.putText(frame, text_coords, (int(x1), int(y2) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Shows the frame on the screen
    cv2.imshow('frame', frame)

    # Wait for a keyboard event to brake or space
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord(' '):
        follow_mouse = not follow_mouse

# Release the resources
cv2.destroyAllWindows()
