# ------- Import Libraries ---------------------------------------------------------------------------------------------------
import cv2
import json
import zenoh
import torch
import numpy as np

# ------- Zenoh ---------------------------------------------------------------------------------------------------

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

# ------- Get Data  ---------------------------------------------------------------------------------------------------
while True:
    for cam in list(cams):
        frame = cams[cam]
        # displaying the frame
        cv2.imshow(str(cam), frame)

    # Wait for a keyboard event to brake
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
cv2.destroyAllWindows()
sub.undeclare()
z.close()