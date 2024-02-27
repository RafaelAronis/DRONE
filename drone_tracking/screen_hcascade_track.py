# ------- Import ---------------------------------------------------------------------------------------------------
import os
import cv2
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
Cascade = cv2.CascadeClassifier("models/drone.xml") # Creates the obj detector
window_title  = "ChatGPT - Google Chrome" #  Window capture title
classes = ['Drone'] # Classes to detect
mouse = Controller()

while True:

    # Frame preparation
    frame = get_chrome_screenshot()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert frame to grayscale

    # Detect objects in frame
    objs = Cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=20,
        minSize=(24, 24),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

     # Draw a rectangle around the objects
    for (x, y, w, h) in objs:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Shows the frame on the screen
    cv2.imshow('screen', frame)

    # Wait for a keyboard event to brake
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
cv2.destroyAllWindows()
