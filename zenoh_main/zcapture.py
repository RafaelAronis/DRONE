import zenoh
import cv2
import json
import imutils
# from email.policy import default
from imutils.video import VideoStream

# ------- Zenoh ---------------------------------------------------------------------------------------------------

# Parameters
IP = '0.0.0.0'
PORT = '7447'
mode = 'peer' # Zenoh session mode ('peer' or 'client')
listen = [f"tcp/{IP}:{PORT}"] # Zenoh endpoints to listen on
quality = 90 # Quality of the published frames (0 - 100)
width = 500 # width of the published frames
key = 'demo/zcam' # Key expression

# Zenoh config
conf = zenoh.Config()
conf.insert_json5(zenoh.config.MODE_KEY, json.dumps(mode))
conf.insert_json5(zenoh.config.LISTEN_KEY, json.dumps(listen))
zenoh.init_logger()
z = zenoh.open(conf)

# ------- Send Data ---------------------------------------------------------------------------------------------------
CAMERA_ID = 0
vs = VideoStream(src=CAMERA_ID).start()
jpeg_opts = [int(cv2.IMWRITE_JPEG_QUALITY), quality]

while True:

    # Frame preparation
    raw = vs.read()
    if raw is not None:
        frame = imutils.resize(raw, width=width)
        _, jpeg = cv2.imencode('.jpg', frame, jpeg_opts)
        z.put(key, jpeg.tobytes())
