# Raspberry Remote Conection

### Conect to Raspberry:
```bash
ssh drone@"IPRaspberry"
dronedrone
cd ./Desktop/CODE
```

### Transfer file from PC to Raspberry
```bash
scp utils.py drone@192.168.19.98:~/Desktop/transfer.py
```

### Transfer file from Raspberry to PC
```bash
scp usuário@IP_RaspberryPi:/home/pi/arquivo.txt .
```
### Transfer folder from PC to Raspberry
```bash
scp -r minha_pasta pi@raspberry_pi_ip:~
```