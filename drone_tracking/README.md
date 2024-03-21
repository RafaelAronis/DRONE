## Capture Imgs
### Terminal 1:
```bash
ssh pi@"IP_TurtleBot3"
raspberry
cd ./zenoh-demos/computer-vision/zcam/zcam-python
python3 zcapture.py -m peer -l tcp/0.0.0.0:7447
```

### Terminal 2:
```bash
cd generate_captures_turtlebot3/
python3 zdisplay.py -m peer -e tcp/"IP_TurtleBot3":7447
```
-------------------------------

## Send local messages

### Terminal 1 Zenoh
```bash
zenoh-0.7.0-rc-x86_64-pc-windows-msvc/zenohd -l tcp/localhost:7447
```

### Terminal 2 Sub
```bash
python3 z_sub.py -l tcp/localhost:7447 -m client -k /demo/example/test
```

### Terminal 3 Pub:
```bash
python3 z_pub.py -e tcp/localhost:7447 -m client -k /demo/example/test -v "str"
```


-------------------------------

## Send messages for Turtlebot3
```bash
python3 z_pub.py -e tcp/A:7447 -m client -k /demo/example/test -v "Str"
zenoh-0.7.0-rc-x86_64-pc-windows-msvc/zenohd -l tcp/B:7447
```