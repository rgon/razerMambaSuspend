#!/usr/bin/env python3
# A simple program that locks your computer (or executes any given command) when you dock your Razer Mamba mouse (and put it into charging mode).
# This solves the problem of forgetting to charge your mouse when AFK, and both actions are combined into one.

# Copyright 2018 Gonzalo Ruiz aka rgon ( github.com/rgon ).

# ocdcastle
# Imports and configurable params.
# !ocdcastle

from pydbus import SessionBus                                                  # sudo pip3 install pydbus
from gi.repository import GLib

import time
import subprocess

import json             # Config file parsing.
import os               # Getting the current directory.

session_bus = SessionBus()                                                     # get the session bus

maxDBUSsearchPings = 5
DBUSsearchSleepTime = int(3)                                                            # seconds.

chargingScanInterval = 1   # seconds.
scan = True

# ocdcastle
# Configuration.
# !ocdcastle

configfile = json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")))

onChargingCommand = configfile["onChargingCommand"]         # Action performed on a mouse dock event.
deviceSerial = configfile["deviceSerial"]

if(configfile["chargingScanInterval"]):
    chargingScanInterval = int(configfile["chargingScanInterval"])

# ocdcastle
# Main functionality.
# !ocdcastle

def connectDBUS(_addr, _interface, _pingNumber):
    global maxDBUSsearchPings, DBUSsearchSleepTime

    if(not _pingNumber):
        _pingNumber = maxDBUSsearchPings
        
    i = 0
    while (i < _pingNumber):                                                   # until return
        try:
            module = session_bus.get(_addr, _interface)

        except:
            if(_pingNumber > 1):
                print("The openrazer daemon doesn't seem to be running. Retrying.")

            i+=1
            if(_pingNumber > 1):
                time.sleep(DBUSsearchSleepTime)
        else:
            print("Successfully communicated with {}".format(_addr))
            return module
    
    # DBSU connection failed.
    print("ERROR: Couldn't connect to {}".format(_addr))
    return None

def connectRazerDriver(_device):
    return connectDBUS("org.razer", "/org/razer/device/{}".format(_device), 0)

def startScanning():
    global scan, chargingScanInterval, onChargingCommand

    print("Scanning each {}s.".format(chargingScanInterval))

    performed = False
    while(scan):
        if(razerMamba.isCharging()):
            if(not performed):
                subprocess.Popen(onChargingCommand, shell=True)
                performed = True
        else:
            performed = False
        
        time.sleep(chargingScanInterval)

# ocdcastle
# Initialization.
# !ocdcastle

# Single-threaded FTW.

if(__name__ == "__main__"):
    razerMamba = connectRazerDriver(deviceSerial)
    if(not razerMamba):
        quit()
    
    print("READY.")
    
    startScanning()