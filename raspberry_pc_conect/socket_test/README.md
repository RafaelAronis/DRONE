## Raspberry Remote Conection
### Terminal 1:
```bash
ssh drone@"IPRaspberry"
dronedrone
cd ./Desktop/CODE./Desktop/CODE/raspberry_pc_conect/socket_test
python rpi_send_socket.py
```

### Terminal 2:
```bash
cd raspberry_pc_conect/socket_test
python pc_get_socket.py
```
