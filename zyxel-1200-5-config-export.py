#!/usr/bin/env python3

#
# Config export script for zyxel 1200-5 switch.
# Gerry Gosselin
# Created 10/22/2021 - Initial commit.
# Edited 6/25/2022 - Comments and some renaming for clarification.
#
# This script works on two types of files.
# 1. A config backup file downloaded from the switch's web interface.
# 2. A dump of the external flash ROM.
#
# This script extracts the admin password, IP address, subnet mask,
# gateway, and hostname.
#
# A note about the admin password. It's encoded poorly. Multiple
# characters encode to the same value. Therefore, when decodng
# the password it may not look like what you expect but it works.
#
# Admin password encoding rules:
# 1. case insensitive
# 2. 5-9 and a-e encode to the sale value
#

import socket
import sys

admin_pw_encoding = [
    '', '0', '1', '2', '3', '4', '5', '6',
    '7', '8', '9', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
    's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    ]

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    sys.exit("Provide a config backup or flash dump file as an argument.")


#
# Decode admin password. Seek to the correct position.
# Read 15 bytes. Decode characters and append to the
# return value. 
#
def get_password(offset):
    config.seek(offset)
    pw_bytes = config.read(15)

    password = ""
    for b in pw_bytes:
        if b==0: break
        password += admin_pw_encoding[b]
    return password


#
# Get IP Address (IP, netmask, or gateway).
# Seek to the correct position. Read 4 bytes.
# Convert ntoa and return.
#
def get_ipaddress(offset):
    config.seek(offset)
    return socket.inet_ntoa(config.read(4))


#
# Get hostname. Seek to the correct position.
# Read 14 bytes. Decode to ascii and return.
#
def get_hostname(offset):
    config.seek(offset)
    return config.read(14).decode('ascii')


#
# Open config or flash file. Read the first 3 bytes.
# If the bytes are 495449, it's a config backup.
# If the bytes are 004002, it's a flash dump.
# If the bytes are 123456, it's a firmware file (throw error).
#
# Seek to the correct position within the file
# and start decoding the values.
#
with open(filename, "rb") as config:

    start = config.read(3).hex()

    if start == "495449": # Config backup file
        print("{0:13} {1}".format("Password:", get_password(65)))
        print("{0:13} {1}".format("IP Address:", get_ipaddress(5)))
        print("{0:13} {1}".format("Subnet Mask:", get_ipaddress(9)))
        print("{0:13} {1}".format("Gateway:", get_ipaddress(13)))
        print("{0:13} {1}".format("Hostname:", get_hostname(23)))

    elif start == "004002": # Flash dump file
        print("{0:13} {1}".format("Password:", get_password(2093121)))
        print("{0:13} {1}".format("IP Address:", get_ipaddress(2093061)))
        print("{0:13} {1}".format("Subnet Mask:", get_ipaddress(2093065)))
        print("{0:13} {1}".format("Gateway:", get_ipaddress(2093069)))
        print("{0:13} {1}".format("Hostname:", get_hostname(2093079)))

    elif start == "123456": # Firmware file
        sys.exit("Firmware files don't have the current config. Choose a flash dump or config backup.")
    else:
        sys.exit("Unknown binary file")
