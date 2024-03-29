# Drone track External Processing

### Terminal 1:
```bash
ssh drone@"IPRaspberry"
dronedrone
cd ./Desktop/CODE/zenoh_main
python rspi_capture_servo.py -p tcp/0.0.0.0:7447 -s tcp/IP_PC:7442
```

### Terminal 2:
```bash
cd ./zenoh_main
python pc_process.py -p tcp/0.0.0.0:7442 -s tcp/IP_RSPI:7447
```
-------------------------------