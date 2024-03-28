# ------- Import Libraries ---------------------------------------------------------------------------------------------------
import cv2
import json
import zenoh
import torch
import socket
import argparse
import numpy as np

# ------- Parser ---------------------------------------------------------------------------------------------------
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

# ------- Socket Servo Conection---------------------------------------------------------------------------------------------------
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f'[INFO] Socket conection at {args.servo_ip}:{args.port_send}...')
client_socket.connect((args.servo_ip, args.port_send))
connection = client_socket.makefile('wb')

# Send data
while True:
    a = str(input())
    data_send = a.encode()
    client_socket.sendall(data_send)