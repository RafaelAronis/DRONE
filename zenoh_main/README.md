# Capture Imgs With zenoh

### Terminal 1: Capturing and Sending Photos from Raspberry Pi to PC
```bash
ssh drone@"IPRaspberry"
dronedrone
cd ./Desktop/CODE/zenoh_main
python z_pc_process_send.py
```

### Terminal 2: Receiving and Executing Commands on Raspberry Pi
```bash
cd ./zenoh_main
python z_pc_process_send.py -l tcp/IPRaspberry:7447
```
-------------------------------

### Terminal 3: Receiving and Sending Commands to Raspberry Pi on PC
```bash
cd ./zenoh_main
python z_pc_process_send.py -l tcp/IPRaspberry:7447
```
-------------------------------