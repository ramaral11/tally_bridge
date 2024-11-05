# tally_bridge
A Python script for the tally function (program only) from Tricaster to Canon CR-N500, if you use SDI (not necessary with NDI).

## How to use
On tricaster: in the channel of the SDI Signal of the camera, go to PTZ, search for Panasonic, and put the Adress of the Raspberry Pi and choose a port (for example 8081);

On Raspberry pi: In this folder, type "python3 tally_bridge.py --port [port] --target-ip [ip of the PTZ Camera] &". 
    For example: python3 tally_bridge.py --port 8081 --target-ip 192.168.1.125 &

The script runs in background. For each camera you must do this. Choose always another Port (and avoid 80 and 8080, because these can have another use.


