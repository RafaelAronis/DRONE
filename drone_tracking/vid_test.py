# ------- Import --------------------------------------------------------------------------
import cv2

# ------- RUN --------------------------------------------------------------------------
Cascade = cv2.CascadeClassifier("cascade/drone.xml") # Creates the obj detector
video_capture = cv2.VideoCapture("data/1.mp4") # Camera video capture

while True:

    # Frame preparation
    ret, frame = video_capture.read() # Reads camera's frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert frame to grayscale

    # Detect objects in frame
    objs = Cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=0,
        minSize=(24, 24),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the objects
    for (x, y, w, h) in objs:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Shows the frame on the screen
    cv2.imshow('camera', frame)

    # Wait for a keyboard event to brake
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
video_capture.release()
cv2.destroyAllWindows()
