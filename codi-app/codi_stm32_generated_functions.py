import logging
import struct

from codi_commands import CoDiCommands
import codi_functions as cf


def read_uint8(p):
    return struct.unpack(">B", p[:1])[0], p[1:]


def read_uint16(p):
    return struct.unpack(">H", p[:2])[0], p[2:]


def read_uint32(p):
    return struct.unpack(">I", p[:4])[0], p[4:]


def read_int8(p):
    return struct.unpack(">b", p[:1])[0], p[1:]


def read_int16(p):
    return struct.unpack(">h", p[:2])[0], p[2:]


def read_int32(p):
    return struct.unpack(">i", p[:4])[0], p[4:]


def read_string(p):
    s, np = read_uint32(p)
    if len(np) >= s:
        return np[:s], np[s:]
    else:
        log.error("Error read_ing string %r%r%r", s, ">", len(np))
        return "", p


def read_utf8_string(p):
    return read_string(p)


def read_blob(p):
    return read_string(p)


log = logging.getLogger("codi-app: ({})".format(__name__))


def readMessage(msg):
    cmdId, msg = read_uint32(msg)
    # log.info("Got cmdId %r", cmdId)
    sessionId, msg = read_uint32(msg)
    # log.info("Got sessionId %r", sessionId)
    handled = False
    if cmdId == CoDiCommands.CMD_ST32_INFO_CODI_FLASH_VERSION:
        handled = True
        log.info("<- CoDiFlashVersionInfo")
        try:
            version, msg = read_string(msg)
            log.info("version = %r", version)
            cf.CoDiFlashVersionInfo(version)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_INFO_PROTOCOL_VERSION:
        handled = True
        log.info("<- ProtocolVersionInfo")
        try:
            majorVer, msg = read_uint8(msg)
            minVer, msg = read_uint8(msg)
            log.info("majorVer = %r", majorVer)
            log.info("minVer = %r", minVer)
            cf.ProtocolVersionInfo(majorVer, minVer)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_BINARY:
        handled = True
        log.info("<- SetBinary")
        try:
            data, msg = read_blob(msg)
            log.info("data = %r", data)
            cf.SetBinary(data)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_S8:
        handled = True
        log.info("<- SetSigned8")
        try:
            num, msg = read_int8(msg)
            log.info("num = %r", num)
            cf.SetSigned8(num)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_RESTART:
        handled = True
        log.info("<- Restart")
        try:
            restartmode, msg = read_uint32(msg)
            log.info("restartmode = %r", restartmode)
            cf.Restart(restartmode)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_DATETIME:
        handled = True
        log.info("<- GetDateTime")
        try:
            cf.GetDateTime()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_LOCATION_STATUS:
        handled = True
        log.info("<- SetLocationStatus")
        try:
            status, msg = read_uint16(msg)
            log.info("status = %r", status)
            cf.SetLocationStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_LOCATION_STATUS:
        handled = True
        log.info("<- GetLocationStatus")
        try:
            cf.GetLocationStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_TORCH_STATUS:
        handled = True
        log.info("<- SetTorchStatus")
        try:
            status, msg = read_uint16(msg)
            log.info("status = %r", status)
            cf.SetTorchStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_TORCH_STATUS:
        handled = True
        log.info("<- GetTorchStatus")
        try:
            cf.GetTorchStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_COVER_STATUS:
        handled = True
        log.info("<- GetCoverStatus")
        try:
            cf.GetCoverStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_WIFI_STATUS:
        handled = True
        log.info("<- SetWiFiStatus")
        try:
            status, msg = read_uint16(msg)
            log.info("status = %r", status)
            cf.SetWiFiStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_WIFI_STATUS:
        handled = True
        log.info("<- GetWiFiStatus")
        try:
            cf.GetWiFiStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_BT_STATUS:
        handled = True
        log.info("<- SetBTStatus")
        try:
            status, msg = read_uint16(msg)
            log.info("status = %r", status)
            cf.SetBTStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_BT_STATUS:
        handled = True
        log.info("<- GetBTStatus")
        try:
            cf.GetBTStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_BATTERY_SAVER_STATUS:
        handled = True
        log.info("<- SetBatterySaverStatus")
        try:
            status, msg = read_uint16(msg)
            log.info("status = %r", status)
            cf.SetBatterySaverStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_BATTERY_SAVER_STATUS:
        handled = True
        log.info("<- GetBatterySaverStatus")
        try:
            cf.GetBatterySaverStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_FLIGHT_MODE_STATUS:
        handled = True
        log.info("<- SetFlightModeStatus")
        try:
            status, msg = read_uint16(msg)
            log.info("status = %r", status)
            cf.SetFlightModeStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_FLIGHT_MODE_STATUS:
        handled = True
        log.info("<- GetFlightModeStatus")
        try:
            cf.GetFlightModeStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_HOTSPOT_STATUS:
        handled = True
        log.info("<- SetHotspotStatus")
        try:
            status, msg = read_uint16(msg)
            log.info("status = %r", status)
            cf.SetHotspotStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_HOTSPOT_STATUS:
        handled = True
        log.info("<- GetHotspotStatus")
        try:
            cf.GetHotspotStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_MOBILE_DATA_STATUS:
        handled = True
        log.info("<- SetMobileDataStatus")
        try:
            status, msg = read_uint16(msg)
            log.info("status = %r", status)
            cf.SetMobileDataStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_MOBILE_DATA_STATUS:
        handled = True
        log.info("<- GetMobileDataStatus")
        try:
            cf.GetMobileDataStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_DND_STATUS:
        handled = True
        log.info("<- SetDoNotDisturbStatus")
        try:
            status, msg = read_uint16(msg)
            log.info("status = %r", status)
            cf.SetDoNotDisturbStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_DND_STATUS:
        handled = True
        log.info("<- GetDoNotDisturbStatus")
        try:
            cf.GetDoNotDisturbStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_VOLUME_LEVEL:
        handled = True
        log.info("<- SetVolumeLevel")
        try:
            status, msg = read_uint16(msg)
            stream, msg = read_uint16(msg)
            log.info("status = %r", status)
            log.info("stream = %r", stream)
            cf.SetVolumeLevel(status, stream)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_VOLUME_LEVEL:
        handled = True
        log.info("<- GetVolumeLevel")
        try:
            stream, msg = read_uint16(msg)
            log.info("stream = %r", stream)
            cf.GetVolumeLevel(stream)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_BATTERY_LEVEL:
        handled = True
        log.info("<- GetBatteryLevel")
        try:
            cf.GetBatteryLevel()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_INFO_CODI_STATUS:
        handled = True
        log.info("<- codi_statusInfo")
        try:
            mode, msg = read_uint32(msg)
            screen, msg = read_uint32(msg)
            data1, msg = read_uint32(msg)
            log.info("mode = %r", mode)
            log.info("screen = %r", screen)
            log.info("data1 = %r", data1)
            cf.codi_statusInfo(mode, screen, data1)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_LOCK:
        handled = True
        log.info("<- SetLock")
        try:
            status, msg = read_uint16(msg)
            log.info("status = %r", status)
            cf.SetLock(status)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_LOCK_STATUS:
        handled = True
        log.info("<- GetLockStatus")
        try:
            cf.GetLockStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_DISMISS_CALL_SMS:
        handled = True
        log.info("<- DismissCallSMS")
        try:
            sim, msg = read_uint32(msg)
            line, msg = read_uint32(msg)
            msisdn, msg = read_string(msg)
            text, msg = read_utf8_string(msg)
            log.info("sim = %r", sim)
            log.info("line = %r", line)
            log.info("msisdn = %r", msisdn)
            log.info("text = %r", text)
            cf.DismissCallSMS(sim, line, msisdn, text)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_ACTION_UNLOCK:
        handled = True
        log.info("<- ActionUnlock")
        try:
            method, msg = read_uint32(msg)
            strdata, msg = read_string(msg)
            log.info("method = %r", method)
            log.info("strdata = %r", strdata)
            cf.ActionUnlock(method, strdata)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_INFO_ST_CHARGING:
        handled = True
        log.info("<- STChargingInfo")
        try:
            status, msg = read_uint32(msg)
            measurement, msg = read_uint32(msg)
            log.info("status = %r", status)
            log.info("measurement = %r", measurement)
            cf.STChargingInfo(status, measurement)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_PLAY_DTMF:
        handled = True
        log.info("<- PlayDTMF")
        try:
            ascii_num, msg = read_uint8(msg)
            log.info("ascii_num = %r", ascii_num)
            cf.PlayDTMF(ascii_num)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SEND_DTMF:
        handled = True
        log.info("<- SendDTMF")
        try:
            sim, msg = read_uint32(msg)
            line, msg = read_uint32(msg)
            asciinum, msg = read_uint8(msg)
            playit, msg = read_uint8(msg)
            log.info("sim = %r", sim)
            log.info("line = %r", line)
            log.info("asciinum = %r", asciinum)
            log.info("playit = %r", playit)
            cf.SendDTMF(sim, line, asciinum, playit)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_ACTION_CALL:
        handled = True
        log.info("<- ActionCall")
        try:
            action, msg = read_uint32(msg)
            sim, msg = read_uint32(msg)
            line, msg = read_uint32(msg)
            numtype, msg = read_uint32(msg)
            msisdn, msg = read_string(msg)
            contact, msg = read_utf8_string(msg)
            contact_id, msg = read_string(msg)
            log.info("action = %r", action)
            log.info("sim = %r", sim)
            log.info("line = %r", line)
            log.info("numtype = %r", numtype)
            log.info("msisdn = %r", msisdn)
            log.info("contact = %r", contact)
            log.info("contact_id = %r", contact_id)
            cf.ActionCall(action, sim, line, numtype, msisdn, contact, contact_id)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SEND_TELE_CODE:
        handled = True
        log.info("<- SendTeleCode")
        try:
            sim, msg = read_uint32(msg)
            line, msg = read_uint32(msg)
            telecode, msg = read_string(msg)
            log.info("sim = %r", sim)
            log.info("line = %r", line)
            log.info("telecode = %r", telecode)
            cf.SendTeleCode(sim, line, telecode)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_CALL_MUTE_STATUS:
        handled = True
        log.info("<- SetCallMuteStatus")
        try:
            status, msg = read_uint32(msg)
            log.info("status = %r", status)
            cf.SetCallMuteStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_CALL_MUTE_STATUS:
        handled = True
        log.info("<- GetCallMuteStatus")
        try:
            cf.GetCallMuteStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_CALL_OUTPUT:
        handled = True
        log.info("<- SetCallOutput")
        try:
            status, msg = read_uint32(msg)
            log.info("status = %r", status)
            cf.SetCallOutput(status)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_CALL_OUTPUT:
        handled = True
        log.info("<- GetCallOutput")
        try:
            cf.GetCallOutput()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_CALL_OUTPUT_OPTIONS:
        handled = True
        log.info("<- GetCallOutputOptions")
        try:
            cf.GetCallOutputOptions()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_ACTION_CAMERA:
        handled = True
        log.info("<- ActionCamera")
        try:
            action, msg = read_uint32(msg)
            log.info("action = %r", action)
            cf.ActionCamera(action)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_CAMERA_FRAME:
        handled = True
        log.info("<- GetCameraFrame")
        try:
            cf.GetCameraFrame()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_CAMERA_SETTINGS:
        handled = True
        log.info("<- SetCameraSettings")
        try:
            parameter, msg = read_uint32(msg)
            value, msg = read_uint32(msg)
            log.info("parameter = %r", parameter)
            log.info("value = %r", value)
            cf.SetCameraSettings(parameter, value)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_CAMERA_CAPTURE_IMAGE:
        handled = True
        log.info("<- CameraCaptureImage")
        try:
            cf.CameraCaptureImage()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_ACTION_VIDEO:
        handled = True
        log.info("<- ActionVideo")
        try:
            action, msg = read_uint32(msg)
            log.info("action = %r", action)
            cf.ActionVideo(action)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_VIDEO_FRAME:
        handled = True
        log.info("<- GetVideoFrame")
        try:
            cf.GetVideoFrame()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_VIDEO_SETTINGS:
        handled = True
        log.info("<- SetVideoSettings")
        try:
            parameter, msg = read_uint32(msg)
            value, msg = read_uint32(msg)
            log.info("parameter = %r", parameter)
            log.info("value = %r", value)
            cf.SetVideoSettings(parameter, value)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_VIDEO_CAPTURE_IMAGE:
        handled = True
        log.info("<- VideoCaptureImage")
        try:
            cf.VideoCaptureImage()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_COVER_LIGHT_SENSOR:
        handled = True
        log.info("<- GetCoverLightSensor")
        try:
            cf.GetCoverLightSensor()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_INFO_CURRENT_LANGUAGE:
        handled = True
        log.info("<- CurrentLanguageInfo")
        try:
            langid, msg = read_string(msg)
            hasallresources, msg = read_uint32(msg)
            data1, msg = read_uint32(msg)
            log.info("langid = %r", langid)
            log.info("hasallresources = %r", hasallresources)
            log.info("data1 = %r", data1)
            cf.CurrentLanguageInfo(langid, hasallresources, data1)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_INFO_MEDIA_RESOURCE:
        handled = True
        log.info("<- MediaResourceInfo")
        try:
            typestr, msg = read_string(msg)
            resname, msg = read_string(msg)
            length, msg = read_uint32(msg)
            status, msg = read_uint32(msg)
            log.info("typestr = %r", typestr)
            log.info("resname = %r", resname)
            log.info("length = %r", length)
            log.info("status = %r", status)
            cf.MediaResourceInfo(typestr, resname, length, status)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_INFO_MEDIA_ACTIVITY:
        handled = True
        log.info("<- MediaActivityInfo")
        try:
            typestr, msg = read_string(msg)
            resname, msg = read_string(msg)
            status, msg = read_uint32(msg)
            log.info("typestr = %r", typestr)
            log.info("resname = %r", resname)
            log.info("status = %r", status)
            cf.MediaActivityInfo(typestr, resname, status)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_INFO_ALERT:
        handled = True
        log.info("<- AlertInfo")
        try:
            status, msg = read_uint32(msg)
            response, msg = read_uint32(msg)
            responsestr, msg = read_utf8_string(msg)
            log.info("status = %r", status)
            log.info("response = %r", response)
            log.info("responsestr = %r", responsestr)
            cf.AlertInfo(status, response, responsestr)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_ORIENTATION:
        handled = True
        log.info("<- GetOrientation")
        try:
            cf.GetOrientation()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_CALL_HISTORY:
        handled = True
        log.info("<- GetCallHistory")
        try:
            index, msg = read_uint32(msg)
            log.info("index = %r", index)
            cf.GetCallHistory(index)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_CONTACTS:
        handled = True
        log.info("<- GetContacts")
        try:
            index, msg = read_uint32(msg)
            log.info("index = %r", index)
            cf.GetContacts(index)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_ACTION_PLAYER:
        handled = True
        log.info("<- ActionPlayer")
        try:
            action, msg = read_uint32(msg)
            log.info("action = %r", action)
            cf.ActionPlayer(action)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_ACTION_NOTIFICATION:
        handled = True
        log.info("<- ActionNotification")
        try:
            notid, msg = read_uint32(msg)
            action, msg = read_uint32(msg)
            pos, msg = read_uint32(msg)
            log.info("notid = %r", notid)
            log.info("action = %r", action)
            log.info("pos = %r", pos)
            cf.ActionNotification(notid, action, pos)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_LEDISON_PATTERN:
        handled = True
        log.info("<- GetLEDisonPattern")
        try:
            contactid, msg = read_string(msg)
            contactname, msg = read_utf8_string(msg)
            msisdn, msg = read_string(msg)
            log.info("contactid = %r", contactid)
            log.info("contactname = %r", contactname)
            log.info("msisdn = %r", msisdn)
            cf.GetLEDisonPattern(contactid, contactname, msisdn)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_LEDISON_MODE:
        handled = True
        log.info("<- GetLEDisonMode")
        try:
            cf.GetLEDisonMode()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_CONTACT_ICON:
        handled = True
        log.info("<- GetContactIcon")
        try:
            contactid, msg = read_string(msg)
            contactname, msg = read_utf8_string(msg)
            msisdn, msg = read_string(msg)
            log.info("contactid = %r", contactid)
            log.info("contactname = %r", contactname)
            log.info("msisdn = %r", msisdn)
            cf.GetContactIcon(contactid, contactname, msisdn)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_MODEM_SIGNAL_INFO:
        handled = True
        log.info("<- GetModemSignalInfo")
        try:
            cf.GetModemSignalInfo()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_DATE_TIME_FORMAT:
        handled = True
        log.info("<- GetDateTimeFormat")
        try:
            cf.GetDateTimeFormat()
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_GET_ALBUM_ART:
        handled = True
        log.info("<- GetAlbumArt")
        try:
            mediasessionformat, msg = read_blob(msg)
            log.info("mediasessionformat =", mediasessionformat)
            cf.GetAlbumArt(mediasessionformat)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_ACTION_VOICE_RECODER:
        handled = True
        log.info("<- ActionVoiceRecorder")
        try:
            action, msg = read_uint32(msg)
            log.info("action = %r", action)
            cf.ActionVoiceRecorder(action)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_SET_VOICE_RECORDER_SETTINGS:
        handled = True
        log.info("<- SetVoiceRecorderSettings")
        try:
            parameter, msg = read_uint32(msg)
            value, msg = read_uint32(msg)
            log.info("parameter = %r", parameter)
            log.info("value = %r", value)
            cf.SetVoiceRecorderSettings(parameter, value)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_ST32_DATA_CHANGE_ALERT:
        handled = True
        log.info("<- STDataChangeAlert")
        try:
            type, msg = read_uint32(msg)
            data1, msg = read_uint32(msg)
            log.info("type = %r", type)
            log.info("data1 = %r", data1)
            cf.STDataChangeAlert(type, data1)
        except Exception as e:
            log.error(e)

    if cmdId == CoDiCommands.CMD_SYNC_SYS_SLEEP_STATUS:
        handled = True
        log.info("<- CoDiOFF")
        try:
            par1, msg = read_uint8(msg)
            log.info("par1 = %r", par1)
            par2, msg = read_uint8(msg)
            log.info("par2 = %r", par2)
            cf.CoDiOFF(par1, par2)
        except Exception as e:
            log.error(e)

    if cmdId == 147:
        handled = True
        log.info("<- MouseInfo")
        try:
            mode, msg = read_uint8(msg)
            log.info("mode = %r", mode)
            x_coord, msg = read_int16(msg)
            log.info("x_coord = %r", x_coord)
            y_coord, msg = read_int16(msg)
            log.info("y_coord = %r", y_coord)
            cf.MouseInfo(mode, x_coord, y_coord)
        except Exception as e:
            log.error(e)

    if cmdId == 148:
        handled = True
        log.info("<- MouseInfo2")
        try:
            pressState, msg = read_uint8(msg)
            log.info("pressState = %r", pressState)
            previousState, msg = read_uint8(msg)
            log.info("previousSatate = %r", previousState)
            x_coord, msg = read_uint16(msg)
            log.info("x_coord = %r", x_coord)
            y_coord, msg = read_uint16(msg)
            log.info("y_coord = %r", y_coord)
            cf.MouseInfo2(pressState, previousState, x_coord, y_coord)
        except Exception as e:
            log.error(e)

    if not handled:
        log.info("<- Unrecognised command %r", cmdId)
