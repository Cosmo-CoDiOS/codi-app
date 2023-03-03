#!/usr/bin/env python3
import logging
import signal
import sys

# import addressbook
import codi_functions as cf
import codi_mtk_generated_functions as mtk_cmd
import codi_status
import dbus_server
import event_listener
import led_manager
import lock_file
import serial_port_manager as serial_port
from codi_generated_parser import *

log = logging.getLogger("codi-app")
logging.basicConfig(level=logging.DEBUG)

CodiStatus: codi_status.CoDiStatus = codi_status.CoDiStatus()
SerialPort: serial_port.SerialPort = serial_port.SerialPort()


def signal_handler(_signo, _stack_frame):
    # mtk_cmd.SetMouse(0, 1)
    mtk_cmd.Setcodi_status(3, 3, 3)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)

lock = "/tmp/.codi.lock"
lock_file.check_and_kill(lock)
lock_file.lock(lock)


def initCodi():
    #    addressbook.refresh_contacts()
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


def main():
    if args["command"]:
        if args["command"] == "dbus":
            try:
                dbus_server.init(False)
                eval(args["cmd"])
            except Exception as e:
                print(e)
            SerialPort.stop_serial()
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
            SerialPort.stop_serial()
            exit(0)

    log.info("codi-app initializing...")

    SerialPort.stop_serial()
    event_listener.init()
    initCodi()

    dbus_server.init()


if __name__ == "__main__":
    main()
