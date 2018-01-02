#!/usr/bin/env python3
# A simple program that locks your computer (or executes any given command) when you dock your Razer Mamba mouse (and put it into charging mode).
# This solves the problem of forgetting to charge your mouse when AFK, and both actions are combined into one.

# Copyright 2018 Gonzalo Ruiz aka rgon ( github.com/rgon ).

############################################################
#                                                          #
#             Imports and configurable params.             #
#                                                          #
############################################################

from pydbus import SessionBus                                                  # sudo pip3 install pydbus
from gi.repository import GLib

import time
import subprocess

import json                                                                    # Config file parsing.
import os                                                                      # Getting the current directory.

import logging

session_bus = SessionBus()                                                     # get the session bus

maxDBUSsearchPings = 5
DBUSsearchSleepTime = int(3)                                                   # seconds.

chargingScanInterval = 1                                                       # seconds.
scan = True

############################################################
#                                                          #
#                      Configuration.                      #
#                                                          #
############################################################

programdir = os.path.dirname(os.path.realpath(__file__))

logfile = os.path.join(programdir, "logs")
logging.basicConfig(filename=logfile, level=logging.DEBUG)

configfile = os.path.join(programdir, "local/config.json")

if(not os.path.isfile(configfile)):                                            # The local/config.json file takes priority, for development purposes.
    configfile = os.path.join(programdir, "config.json")

try:
    configfile = json.load(open( configfile ))
except Exception as e:
    logging.info("ERROR reading the config.json file: {}".format(e))
    quit()

onChargingCommand = configfile["onChargingCommand"]                            # Action performed on a mouse dock event.
deviceSerial = configfile["deviceSerial"]

if(configfile["chargingScanInterval"]):
    chargingScanInterval = int(configfile["chargingScanInterval"])

############################################################
#                                                          #
#                    Main functionality.                   #
#                                                          #
############################################################

def connectDBUS(_addr, _interface, _pingNumber):
    global maxDBUSsearchPings, DBUSsearchSleepTime

    if(not _pingNumber):
        _pingNumber = maxDBUSsearchPings
        
    i = 0
    while (i < _pingNumber):                                                   # until return
        try:
            module = session_bus.get(_addr, _interface)

        except Exception as e:
            if(_pingNumber > 1):
                logging.critical("The openrazer daemon doesn't seem to be running. Retrying. Error: {}".format(e))

            i+=1
            if(_pingNumber > 1):
                time.sleep(DBUSsearchSleepTime)
        else:
            logging.info("Successfully communicated with {}".format(_addr))
            return module
    
    # DBSU connection failed.
    logging.critical("ERROR: Couldn't connect to {}".format(_addr))
    return None

def connectRazerDriver(_device):
    return connectDBUS("org.razer", "/org/razer/device/{}".format(_device), 0)

def startScanning():
    global scan, chargingScanInterval, onChargingCommand

    logging.info("Scanning each {}s.".format(chargingScanInterval))

    performed = False
    while(scan):
        if(razerMamba.isCharging()):
            if(not performed):
                subprocess.Popen(onChargingCommand, shell=True)
                performed = True
        else:
            performed = False
        
        time.sleep(chargingScanInterval)

############################################################
#                                                          #
#                      Initialization.                     #
#                                                          #
############################################################

# Single-threaded FTW.

if(__name__ == "__main__"):
    logging.info("Starting.")

    razerMamba = connectRazerDriver(deviceSerial)
    if(not razerMamba):
        quit()
    
    logging.info("READY.")
    
    startScanning()