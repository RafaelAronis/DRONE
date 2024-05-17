# Raspberry Remote Conection

### Conect to Raspberry:
```bash
ssh drone@"IPRaspberry"
ssh drone@"IPRaspberry"
dronedrone
cd ./Desktop/CODE
```

### Transfer file from PC to Raspberry
```bash
scp utils.py drone@192.168.19.98:~/Desktop/transfer.py
scp -r zenoh_main/rspi_capture_servo.py drone@192.168.107.98:~/Desktop/CODE/zenoh_main/rspi_capture_servo.py
scp -r zenoh_main/utils_main/utils_RSPI.py drone@192.168.107.98:~/Desktop/CODE/zenoh_main/utils_RSPI.py
scp -r stepper_motor/test1.py drone@192.168.107.98:~/Desktop/test1.py
```

### Transfer file from Raspberry to PC
```bash
scp drone@IP_RaspberryPi:/home/pi/arquivo.txt .
```
### Transfer folder from PC to Raspberry
```bash
scp -r minha_pasta pi@raspberry_pi_ip:~
scp -r zenoh_main/ drone@192.168.107.98:~/Desktop/CODE/zenoh_main

```