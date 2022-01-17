import logging

import addressbook
import codi_functions as cf
import codi_mtk_generated_functions as mtk_cmd
import codi_status
import dbus_server
import led_manager

log = logging.getLogger("codi")


def init():
    global CallInfo
    global DeviceInfo
    CallInfo = codi_status.CallInfo
    DeviceInfo = codi_status.DeviceInfo


def volumeButtonPressed(sender, name, value):
    log.info("<= %r %r %r", sender, name, value)

    if name == "decrease_volume":
        if CallInfo.state == "incoming":
            try:
                CallInfo.currentCall.Answer()
            except Exception as e:
                log.error(e)
        else:
            mtk_cmd.KeyPressInfo(25, value, 0)
    if name == "increase_volume":
        if CallInfo.state in ("alerting", "incoming", "active", "dialing"):
            try:
                CallInfo.currentCall.Hangup()
            except Exception as e:
                log.error(e)
        else:
            mtk_cmd.KeyPressInfo(24, value, 0)


def propertiesChanged(sender, property, data):
    log.info("<= %r %r %r", sender, property, data)
    if "LidIsClosed" in property.keys():
        value = property["LidIsClosed"]
        DeviceInfo.lidClosed = value

        if CallInfo.state == "disconnected":
            if value:
                mtk_cmd.Setcodi_status(1, 0, 1)
                led_manager.ledsBlue()
                mtk_cmd.SetMouse(0, 1)
            else:
                mtk_cmd.Setcodi_status(1, 7, 1)
                led_manager.ledsOff()
                mtk_cmd.SetMouse(1, 1)
    if "Energy" in property and "EnergyFull" in property:
        energy = property["Energy"]
        eFull = property["EnergyFull"]
        DeviceInfo.batteryLevel = int(energy * 100 / eFull)
        cf.GetBatteryLevel()
        led_manager.ledsCharging(dbus_server.power.State == 1)


def networkPropertiesChanged(properties):
    log.info("<= %r", properties)
    mtk_cmd.WiFiStatusInfo(int(dbus_server.network.WirelessEnabled), 100)


def propertyChanged(property, value):
    log.info("<=", property, value)
    # TODO: This does NOT work for some reason!
    if property == "Muted":
        mtk_cmd.CallMuteStatusInfo(1)
    if property == "State":
        CallInfo.state = value
        if value == "active":
            mtk_cmd.CallInfo(
                CallInfo.modemId, 2, "0", CallInfo.contactName, CallInfo.msisdn, 0
            )
        if value == "disconnected":
            mtk_cmd.CallInfo(
                CallInfo.modemId, 0, "0", CallInfo.contactName, CallInfo.msisdn, 0
            )
            mtk_cmd.MTKDataChangeAlert(1, 0)
            if DeviceInfo.lidClosed:
                led_manager.ledsBlue()
            else:
                led_manager.ledsOff()
            cf.SetCallOutput(0)


def callStatusChanged(sender, data=None):
    log.info("<=", sender, data)
    if data:
        CallInfo.currentCall = dbus_server.bus.get("org.ofono", sender)
        CallInfo.currentCall.onPropertyChanged = propertyChanged
        CallInfo.state = data["State"]
        if data["State"] in ["incoming", "dialing"]:
            CallInfo.modemId = 0
            if "/ril_1" in sender:
                CallInfo.modemId = 1
            CallInfo.contactName = data["Name"]
            CallInfo.msisdn = data["LineIdentification"]
            if CallInfo.contactName == "":
                CallInfo.contactName = addressbook.contactNameForNumber(CallInfo.msisdn)
            led_manager.ledsIncomingCall()
            if data["State"] == "incoming":
                mtk_cmd.CallInfo(
                    CallInfo.modemId, 1, "0", CallInfo.contactName, CallInfo.msisdn, 0
                )
            else:
                mtk_cmd.CallInfo(
                    CallInfo.modemId, 13, "0", CallInfo.contactName, CallInfo.msisdn, 0
                )
