import sys
import json
import time
import zenoh
import argparse

# --- Command line argument parsing --- --- --- --- --- ---
parser = argparse.ArgumentParser(
    prog='z_pc_process_send',
    description='zenoh video capture example')
parser.add_argument('-l', '--connect', type=str, default='tcp/192.168.222.98:7447',
                    help='zenoh endpoints to listen on (raspi IP and port).')
parser.add_argument('-s', '--servo_ip', type=str, default=parser.parse_args().connect.split('/')[1].split(':')[0],
                    help='zenoh endpoints to listen on (raspi IP and port).')
parser.add_argument('-p', '--port_send', type=int, default=12345,
                    help='scket send port')
parser.add_argument('-k', '--key', type=str, default='demo/zcam',
                    help='key expression')
parser.add_argument('-m', '--model_path', type=str, default='models/best.pt',
                    help='model used path')

args = parser.parse_args()


# Zenoh code  --- --- --- --- --- --- --- --- --- --- ---

def callback(sample: zenoh.Sample):
    print(f"{sample.payload.decode('utf-8')}")


# "Open" zenoh


conf = zenoh.Config()
conf.insert_json5(zenoh.config.MODE_KEY, json.dumps('peer'))
conf.insert_json5(zenoh.config.CONNECT_KEY, json.dumps([args.connect]))
print(f'[INFO] Open zenoh session at {args.connect} ...')
zenoh.init_logger()
session = zenoh.open(conf) # open session
sub = session.declare_subscriber(args.key, callback, reliability=zenoh.Reliability.RELIABLE()) # declare subscriber



# Loop
print("Enter 'q' to quit...",'\n')
c = ''
try:
    while c != 'q':
        c = sys.stdin.read(1)
        time.sleep(1)
except:
    pass
sub.undeclare()
session.close()
