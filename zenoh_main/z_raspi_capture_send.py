# ------- Import ---------------------------------------------------------------------------------------------------
import cv2
import json
import time
import zenoh
import socket
import imutils
import argparse
from email.policy import default
from imutils.video import VideoStream

# ------- Parser ---------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(prog='z_raspi_capture_send.',description='video capture')
parser.add_argument('-l', '--listen', type=str, metavar='ENDPOINT', default='tcp/0.0.0.0:7447',
                    help='zenoh endpoints to listen on.')
parser.add_argument('-k', '--key', type=str, default='demo/zcam',
                    help='key expression')
parser.add_argument('-d', '--delay', type=float, default=0.05,
                    help='delay between each frame in seconds')
parser.add_argument('-q', '--quality', type=int, default=95,
                    help='quality of the published frames (0 - 100)')
parser.add_argument('-w', '--width', type=int, default=500,
                    help='width of the published frames')
args = parser.parse_args()

# ------- Zenoh ---------------------------------------------------------------------------------------------------

# Zenoh config
conf = zenoh.Config()
conf.insert_json5(zenoh.config.MODE_KEY, json.dumps('peer'))
conf.insert_json5(zenoh.config.LISTEN_KEY, json.dumps([args.listen]))
print(f'[INFO] Socket conection at {args.listen}...')
zenoh.init_logger()
z = zenoh.open(conf)

# ------- Send Data ---------------------------------------------------------------------------------------------------
CAMERA_ID = 0
print('[INFO] Open camera...')
vs = VideoStream(src=CAMERA_ID).start()
jpeg_opts = [int(cv2.IMWRITE_JPEG_QUALITY), args.quality]
print(f'[INFO] All done. Endpoint at {socket.gethostbyname(socket.gethostname())}')

while True:

    # Frame preparation
    raw = vs.read()
    if raw is not None:
        frame = imutils.resize(raw, width=args.width)
        _, jpeg = cv2.imencode('.jpg', frame, jpeg_opts)
        z.put(args.key, jpeg.tobytes())
    time.sleep(args.delay)

print('[INFO] Quiting ...')