# Main Project

## Running the Project

### Terminal 1: Capturing and Sending Photos from Raspberry Pi to PC
```bash
ssh drone@"IPRaspberry"
cd ./Desktop/CODE/main
python raspi_capture_send.py
```

### Terminal 2: Receiving and Executing Commands on Raspberry Pi
```bash
ssh drone@"IPRaspberry"
cd ./Desktop/CODE/main
python raspi_receive_execute.py
```

### Terminal 3: Processing Photos and Sending Commands to Raspberry Pi (External PC)
```bash
cd main/
python pc_process_send.py
```
