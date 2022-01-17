#!/usr/bin/env python3
import logging
import signal
import sys

import addressbook
import codi_functions as cf
import codi_mtk_generated_functions as mtk_cmd
import codi_status
import dbus_server
import event_listener
import led_manager
import lock_file
import serial_port_manager
from codi_generated_parser import *

log = logging.getLogger("codi-app ({})".format(__name__))
log.setLevel(logging.DEBUG)


def signalHandler(_signo, _stack_frame):
    # mtk_cmd.SetMouse(0, 1)
    mtk_cmd.Setcodi_status(3, 3, 3)
    sys.exit(0)


signal.signal(signal.SIGINT, signalHandler)
signal.signal(signal.SIGTERM, signalHandler)
signal.signal(signal.SIGABRT, signalHandler)
signal.signal(signal.SIGHUP, signalHandler)

lock = "/tmp/.codi.lock"
lock_file.check_and_kill(lock)
lock_file.lock(lock)

# To turn on console logging uncomment the following line
# logging.basicConfig(level=logging.DEBUG)

log.info("Initializing...")
codi_status.init()


def initCodi():
    addressbook.refreshContacts()
    mtk_cmd.Setcodi_status(1, 7, 1)
    mtk_cmd.SetMouse(1, 1)
    cf.GetDateTime()
    led_manager.leds_off()
    mtk_cmd.DoNotDisturbStatusInfo(0)
    mtk_cmd.BTStatusInfo(0)
    mtk_cmd.WiFiStatusInfo(1, 100)
    mtk_cmd.ModemSignalInfo(1, 0, 0)
    mtk_cmd.MTKDataChangeAlert(1, 0)
    mtk_cmd.MTKDataChangeAlert(0, 0)
    cf.SetCallOutput(0)


serial_port_manager.init()

print("Codi Linux Server")
if args["command"]:
    if args["command"] == "dbus":
        try:
            dbus_server.init(False)
            eval(args["cmd"])
        except Exception as e:
            print(e)
        serial_port_manager.stop()
        exit(0)
    else:
        firstArg = True
        cmd = "mtk_cmd." + args["command"] + "("
        for i in args:
            if i != "command":
                if firstArg:
                    firstArg = False
                else:
                    cmd += ", "
                cmd += str(args[i])
        cmd += ")"
        eval(cmd)
        serial_port_manager.stop()
        exit(0)

event_listener.init()
initCodi()

dbus_server.init()
