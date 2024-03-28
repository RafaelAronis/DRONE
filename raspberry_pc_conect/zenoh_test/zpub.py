import json
import zenoh
import argparse

# --- Command line argument parsing --- --- --- --- --- ---
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

# Zenoh code  --- --- --- --- --- --- --- --- --- --- ---
conf = zenoh.Config()
conf.insert_json5(zenoh.config.MODE_KEY, json.dumps('peer'))
conf.insert_json5(zenoh.config.LISTEN_KEY, json.dumps([args.listen]))
print(f'[INFO] Socket conection at {args.listen}...')
zenoh.init_logger()
z = zenoh.open(conf)

session = zenoh.open(conf)
pub = session.declare_publisher(args.key)

# Code
# Send data
try:
    while True:
        a = str(input())
        pub.put(a)
except:
    pass
print(1)
pub.undeclare()
session.close()
