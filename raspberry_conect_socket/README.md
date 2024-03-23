## Raspberry Remote Conection
### Terminal 1:
```bash
ssh drone@"IPRaspberry"
dronedrone
cd ./Desktop/CODE
python rpi_send_socket.py
```

### Terminal 2:
```bash
cd raspberry_conect/
python pc_get_socket.py
```
-------------------------------

## Transfer file

### Terminal 1 PC:
```bash
scp utils.py drone@192.168.19.98:~/Desktop/transfer.py
scp usuário@IP_RaspberryPi:/home/pi/arquivo.txt .
```