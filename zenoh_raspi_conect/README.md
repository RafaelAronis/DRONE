# Capture Imgs With zenoh

### Terminal 1: Capturing and Sending Photos from Raspberry Pi to PC
```bash
ssh drone@"IPRaspberry"
dronedrone
cd ./Desktop/CODE/zenoh-test
python zcapture.py -m peer -l tcp/0.0.0.0:7447
```

### Terminal 2: Receiving and Executing Commands on Raspberry Pi
```bash
cd ./Desktop/CODE/zenoh-test
python zdisplay.py -m peer -e tcp/"IPRaspberry":7447
```
-------------------------------