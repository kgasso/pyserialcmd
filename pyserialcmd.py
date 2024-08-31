#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Connects to a serial console device and sends commands from a file provided.

Allows you to connect to a serial console device (e.g. router, switch, etc.) and send
commands saved in a file over the serial port. Serial device, file containing commands
to send, baudrate, bytesize, parity, stop bits, etc. can be set via command line 
switches. Use the --help switch to see a full list of parameters.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Kameron Gasso"
__copyright__ = "Copyright 2024, Kameron Gasso"
__license__ = "GPLv3"
__version__ = "1.0.0"
__date__ = "2024/08/30"
__maintainer__ = "Kameron Gasso"
__email__ = "kameron@gasso.org"
__status__ = "Production"

import sys
import serial
import time
import argparse

parser = argparse.ArgumentParser(description='Connect to serial console and send the commands from a file.')

parser.add_argument(
    'SERIALPORT',
    help="serial port name")

parser.add_argument(
    'FILENAME',
    help="filename holding commands to send via serial")
                    
parser.add_argument(
    'BAUDRATE',
    type=int,
    nargs='?',
    help='set baud rate, default: %(default)s',
    default=9600)

group = parser.add_argument_group('serial port')

group.add_argument(
    "--bytesize",
    choices=[5, 6, 7, 8],
    type=int,
    help="set bytesize, one of {5 6 7 8}, default: 8",
    default=8)

group.add_argument(
    "--parity",
    choices=['N', 'E', 'O', 'S', 'M'],
    type=lambda c: c.upper(),
    help="set parity, one of {N E O S M}, default: N",
    default='N')

group.add_argument(
    "--stopbits",
    choices=[1, 1.5, 2],
    type=float,
    help="set stopbits, one of {1 1.5 2}, default: 1",
    default=1)

group.add_argument(
    '--rtscts',
    action='store_true',
    help='enable RTS/CTS flow control (default off)',
    default=False)

group.add_argument(
    '--xonxoff',
    action='store_true',
    help='enable software flow control (default off)',
    default=False)

group.add_argument(
    '--rts',
    type=int,
    help='set initial RTS line state (possible values: 0, 1)',
    default=None)

group.add_argument(
    '--dtr',
    type=int,
    help='set initial DTR line state (possible values: 0, 1)',
    default=None)

args = parser.parse_args()

ser = serial.serial_for_url(args.SERIALPORT, do_not_open=True)
ser.baudrate = args.BAUDRATE
ser.bytesize = args.bytesize
ser.parity = args.parity
ser.stopbits = args.stopbits
ser.rtscts = args.rtscts
ser.xonxoff = args.xonxoff

if args.rts is not None:
    ser.rts = args.rts

if args.dtr is not None:
    ser.dtr = args.dtr

try:
    ser.open()
except serial.SerialException as e:
    sys.stderr.write('Could not open serial port {}: {}\n'.format(ser.name, e))
    sys.exit(1)

with open(args.FILENAME, "rb") as source_file:
    code = compile(source_file.read(), args.FILENAME, "exec")
exec(code)

ser.write(cmd)