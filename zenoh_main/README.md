# Reference
## Data base
> https://drive.google.com/file/d/1YuRWsIc6-GhX2yucxL_HsSplGPPK2mX1/view
## Inspiration 
>https://github.com/emineeminesahin/DroneDetectionWithYOLO/tree/main/yolov5sdetectionresult/exp2

# Drone track External Processing

### Terminal 1:
```bash
ssh drone@"IPRaspberry"
dronedrone
sudo pigpiod
cd ./Desktop/CODE/zenoh_main
python rspi_capture_servo.py -p tcp/0.0.0.0:7447 -s tcp/IP_PC:7442
```

### Terminal 2:
```bash
cd ./zenoh_main
python pc_process.py -p tcp/0.0.0.0:7442 -s tcp/IP_RSPI:7447
```
-------------------------------

# EX

### Terminal 1:
```bash
ssh drone@192.168.107.98
dronedrone
sudo pigpiod
cd ./Desktop/CODE/zenoh_main
python rspi_capture_servo.py -p tcp/0.0.0.0:7447 -s tcp/192.168.107.159:7442
```

### Terminal 2:
```bash
cd ./zenoh_main
python pc_process.py -p tcp/0.0.0.0:7442 -s tcp/192.168.107.98:7447
```
-------------------------------
