# pyserialcmd
Small python script to send a command file to a serial device. I originally wrote this to send scripted commands to a serial-controlled tower light (in my case an ANDONT Stack LED USB Tower Light).

STEP 1: Install required modules (pyserial)

pip install -r requirements.txt


STEP 2: Populate your commands file. This could contain code such as:

#red flash on
cmd = [0xA0, 0x01, 0x01, 0xB3]
cmd = bytearray(cmd)


STEP 3: Execute the command, passing in the serial port and path to the commands file:

pyserialcmd.py COM4 cmds\red-on-flash.py.part

or

pyserialcmd.py /dev/ttyUSB0 cmds/red-on-flash.py.part

You can also pass in other parameters, use pyserialcmd.py --help for a full list.

By no means am I a programmer and I'm brand new to Python... so beware. Hopefully this will help someone out with getting their little project off the ground!
