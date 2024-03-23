# ------- Import Libraries ---------------------------------------------------------------------------------------------------
import cv2
import socket
import struct
import pickle

# ------- Conection ---------------------------------------------------------------------------------------------------
pc_ip = '192.168.16.159'
PORT_SEND = 8485
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((pc_ip, PORT_SEND))
connection = client_socket.makefile('wb')

# ------- Send Data ---------------------------------------------------------------------------------------------------
cam = cv2.VideoCapture(0)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:

    # Frame preparation
    ret, frame = cam.read() # Reads camera's frame
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame, 0)
    size = len(data)
    client_socket.sendall(struct.pack(">L", size) + data)

    # Wait for a keyboard event to brake
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
cam.release()