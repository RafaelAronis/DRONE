## Raspberry Remote Conection
### Terminal 1:
```bash
ssh drone@"IPRaspberry"
dronedrone
cd ./Desktop/CODE
```

### Terminal 2:
```bash
cd generate_captures_turtlebot3/
python3 zdisplay.py -m peer -e tcp/"IP_TurtleBot3":7447
```
-------------------------------

## Transfer file

### Terminal 1 PC:
```bash
scp utils.py drone@192.168.19.98:~/Desktop/transfer.py
```
