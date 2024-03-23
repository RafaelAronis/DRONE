# Capture Imgs With zenoh

### Terminal 1: Capturing and Sending Imgs from Raspberry Pi to PC
```bash
ssh drone@"IPRaspberry"
dronedrone
cd ./Desktop/CODE/raspberry_pc_conect/zenoh_test
python zcapture.py
```

### Terminal 2: Receiving Imgs on PC
```bash
cd raspberry_pc_conect/zenoh_test
python zdisplay.py
```
-------------------------------