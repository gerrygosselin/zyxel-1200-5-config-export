#!/usr/bin/env python3

import socket
import sys

cipher = [
    '', '0', '1', '2', '3', '4', '5', '6',
    '7', '8', '9', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
    's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    ]

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("Provide a config backup or flash dump file as an argument.")
    sys.exit()


def get_password(offset):
    config.seek(offset)
    pw_bytes = config.read(15)

    password = ""
    for b in pw_bytes:
        if b==0: break
        password += cipher[b]
    return password

def get_ipaddress(offset):
    config.seek(offset)
    return socket.inet_ntoa(config.read(4))

def get_hostname(offset):
    config.seek(offset)
    return config.read(14).decode('ascii')


with open(filename, "rb") as config:

    # Determine if this is a config backup
    # or a flash dump. Config backups start
    # with the hex chars 49 54 49.

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

    else:
        print("Unknown binary file")
