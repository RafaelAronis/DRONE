# ------- Import ---------------------------------------------------------------------------------------------------
import cv2
import pickle
import socket
import struct
import numpy as np

# ------- Conection ---------------------------------------------------------------------------------------------------
HOST=''
PORT=8485
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(10)
print('Socket now listening')
conn,addr=s.accept()
data = b""
payload_size = struct.calcsize(">L")

# ------- Get data ---------------------------------------------------------------------------------------------------
while True:

    while len(data) < payload_size:
        data += conn.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    print(frame.shape)
    cv2.imshow('frame',frame)
    cv2.waitKey(1)

    # Wait for a keyboard event to brake
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
cv2.destroyAllWindows()