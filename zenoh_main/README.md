# Capture Imgs With zenoh

### Terminal 1: Capturing and Sending Photos from Raspberry Pi to PC
```bash
ssh drone@"IPRaspberry"
dronedrone
cd ./Desktop/CODE/zenoh-test
python zcapture.py
```

### Terminal 2: Receiving and Executing Commands on Raspberry Pi
```bash
cd ./Desktop/CODE/zenoh-test
python zdisplay.py
```
-------------------------------