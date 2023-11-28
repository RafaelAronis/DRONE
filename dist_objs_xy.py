import cv2
import math

def detect_object(frame, cascade, prev_position=None, threshold=10):

    # Detect object
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    objects = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    if len(objects) == 0:
        return None

    # Build rectangle and center
    largest_object = max(objects, key=lambda x: x[2] * x[3])
    x, y, w, h = largest_object
    cx = x + w // 2
    cy = y + h // 2
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Only update position if within threshold distance from previous position
    if prev_position is not None and math.sqrt((cx - prev_position[0])**2 + (cy - prev_position[1])**2) < threshold:
        return prev_position

    return (cx, cy, w, h)

def move_robot(dx,dy,dz):
    # Control the robot's movement based on the error and dz
    pass

def stop_robot():
    # Stop the robot's movement
    pass

#############################################################################################################

# Open camera
cap = cv2.VideoCapture(0)

# Load cascade
obj_cascade = cv2.CascadeClassifier('cascade/norg/haarcascade_frontalface_default.xml')
# bot_cascade = cv2.CascadeClassifier('cascade/cascade1/cascade.xml')
bot_cascade = cv2.CascadeClassifier('cascade/norg/hand.xml')
obj_position, bot_position = None, None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect objects
    obj_position = detect_object(frame, obj_cascade,obj_position)
    bot_position = detect_object(frame, bot_cascade,bot_position)

    if obj_position and bot_position:
        dx, dy = [obj_position[0] - bot_position[0], obj_position[1] - bot_position[1]]
        dz = (obj_position[2] * obj_position[3] - bot_position[2] * bot_position[3])/10
        angle_to_object = math.atan2(dz, dx) # Angle that the robot needs to turn to align itself with the object

        cv2.arrowedLine(frame, bot_position[:2], obj_position[:2], (0, 255, 0), 2)
        cv2.putText(frame, f"( x: {round(dx,0)}, y: {round(dy,0)}, z: {round(dz,0)}, angle to object: {round(angle_to_object,2)}°)", (30, 35),cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)

        move_robot(dx, dy, dz)
    else:
        stop_robot()

    cv2.imshow("Person following", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
