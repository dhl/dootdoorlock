#!/usr/bin/python
#
# usage:
#   to run: ./door.py
#   to add users: ./door.py add
#
from __future__ import print_function
import os, re, subprocess, serial, signal, sys
from hashlib import sha256 as hashfun
from time import sleep

octopus_reader ="/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0"
ser = serial.Serial(octopus_reader, 9600)
userdata = "users.txt"

class Door:
    def __init__(self, seconds=5):
        self.lock = "/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0"
        self.seconds = seconds

    def open(self):
        p = subprocess.Popen(["cat", doorlock])
        sleep(self.seconds)
        p.terminate()

    def run(self, authfun):
        while True:
            sleep(1)
            if authfun():
                self.open()

def read_users():
    users = dict()
    with open(userdata) as userfile:
        for line in userfile:
	    name, key = line.strip("\n").rsplit(" ", 1)
            users[name] = key
    return users

def save_users(users):
    with open(userdata, 'w') as userfile:
        for name in sorted(users):
            print("{0} {1}".format(name, users[name]), file=userfile)
    print("Saved users")

def add_user():
    users = read_users()
    print("Enter name (lastname firstname) of user to add then press enter.")
    name = raw_input()
    print("Now scan octopus card.")
    key = read_user()
    if name in users:
        print("{0} is already in database. To overwrite type: y".format(name))
        if raw_input().lower() != "y":
	    print("not adding")
            return
    users[name] = key
    save_users(users)

def open_door():

def read_user():
    return hashfun(re.sub("[^0-F]", "", ser.readline())).hexdigest()

def run():
    users = read_users()
    while True:
        key = read_user()
    	if key in users.values():
            print("Opening")
            open_door()

if __name__ == "__main__":
    if len(sys.argv) > 1:
	add_user()
    else:
	run()
