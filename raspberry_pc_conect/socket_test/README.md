## Capture Imgs With socket

### Terminal 1: Capturing and Sending Imgs from Raspberry Pi to PC
```bash
ssh drone@"IPRaspberry"
dronedrone
cd ./Desktop/CODE./Desktop/CODE/raspberry_pc_conect/socket_test
python rpi_send_socket.py
```

### Terminal 2: Receiving Imgs on PC
```bash
cd raspberry_pc_conect/socket_test
python pc_get_socket.py
```
