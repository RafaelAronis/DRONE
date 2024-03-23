## Capture Imgs With socket

### Terminal 1: Capturing and Sending Photos from Raspberry Pi to PC
```bash
ssh drone@"IPRaspberry"
dronedrone
cd ./Desktop/CODE./Desktop/CODE/raspberry_pc_conect/socket_test
python rpi_send_socket.py
```

### Terminal 2: Receiving and Executing Commands on Raspberry Pi
```bash
cd raspberry_pc_conect/socket_test
python pc_get_socket.py
```
