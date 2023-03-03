import logging
import struct

from codi_commands import CoDiCommands
from codi_server import SerialPort

log = logging.getLogger("codi-app: ({})".format(__name__))


def write_uint8(p):
    return struct.pack(">B", p)


def write_uint16(p):
    return struct.pack(">H", p)


def write_uint32(p) -> bytes:
    return struct.pack(">I", p)


def write_int8(p):
    return struct.pack(">b", p)


def write_int16(p):
    return struct.pack(">h", p)


def write_int32(p):
    return struct.pack(">i", p)


def write_string(s):
    return write_uint32(len(s)) + s.encode()


def write_utf8_string(s):
    return write_string(s)


def write_blob(b):
    return write_string(b)


def send_message(commandId, args):
    if args is None:
        args = []

    msgHeader = bytes.fromhex("58 21 58 21")
    cmdId = write_uint32(commandId)
    cmdSessionId = bytes.fromhex("00 00 00 01")
    msgLength = len(msgHeader) + 4 + len(cmdId) + len(cmdSessionId)
    for i in args:
        msgLength += len(i)

    cmd = msgHeader + write_uint32(msgLength) + cmdId + cmdSessionId
    for i in args:
        cmd += i

    SerialPort.send_command(list(cmd))


def GetFlashVersion():
    log.info("-> GetFlashVersion")
    send_message(CoDiCommands.CMD_MTK_GET_CODI_FLASH_VERSION)


def DateTimeInfo(day, month, year, hour, minute, second, tz):
    log.info("-> DateTimeInfo")
    send_message(
        CoDiCommands.CMD_MTK_INFO_DATETIME,
        [
            write_uint32(day),
            write_uint32(month),
            write_uint32(year),
            write_uint32(hour),
            write_uint32(minute),
            write_uint32(second),
            write_uint32(tz),
        ],
    )


def LocationStatusInfo(status):
    log.info("-> LocationStatusInfo")
    send_message(CoDiCommands.CMD_MTK_INFO_LOCATION_STATUS, [write_uint16(status)])


def TorchStatusInfo(status):
    log.info("-> TorchStatusInfo")
    send_message(CoDiCommands.CMD_MTK_INFO_TORCH_STATUS, [write_uint16(status)])


def CoverStatusInfo(status):
    log.info("-> CoverStatusInfo")
    send_message(CoDiCommands.CMD_MTK_INFO_COVER_STATUS, [write_uint16(status)])


def WiFiStatusInfo(status, signalval):
    log.info("-> WiFiStatusInfo")
    send_message(
        CoDiCommands.CMD_MTK_INFO_WIFI_STATUS,
        [write_uint16(status), write_uint32(signalval)],
    )


def BTStatusInfo(status):
    log.info("-> BTStatusInfo")
    send_message(CoDiCommands.CMD_MTK_INFO_BT_STATUS, [write_uint16(status)])


def BatterySaverStatusInfo(status):
    log.info("-> BatterySaverStatusInfo")
    send_message(CoDiCommands.CMD_MTK_INFO_BATTERY_SAVER_STATUS, [write_uint16(status)])


def FlightModeStatusInfo(status):
    log.info("-> FlightModeStatusInfo")
    send_message(CoDiCommands.CMD_MTK_INFO_FLIGHT_MODE_STATUS, [write_uint16(status)])


def HotspotStatusInfo(status):
    log.info("-> HotspotStatusInfo")
    send_message(CoDiCommands.CMD_MTK_INFO_HOTSPOT_STATUS, [write_uint16(status)])


def MobileDataStatusInfo(status):
    log.info("-> MobileDataStatusInfo")
    send_message(CoDiCommands.CMD_MTK_INFO_MOBILE_DATA_STATUS, [write_uint16(status)])


def DoNotDisturbStatusInfo(status):
    log.info("-> DoNotDisturbStatusInfo")
    send_message(CoDiCommands.CMD_MTK_INFO_DND_STATUS, [write_uint16(status)])


def VolumeLevelInfo(status, stream):
    log.info("-> VolumeLevelInfo")
    send_message(
        CoDiCommands.CMD_MTK_INFO_VOLUME_LEVEL,
        [write_uint16(status), write_uint16(stream)],
    )


def BatteryLevelInfo(status):
    log.info("-> BatteryLevelInfo")
    send_message(CoDiCommands.CMD_MTK_INFO_BATTERY_LEVEL, [write_uint16(status)])


def Setcodi_status(mode, screen, data1):
    log.info("-> Setcodi_status")
    send_message(
        CoDiCommands.CMD_MTK_SET_CODI_STATUS,
        [write_uint32(mode), write_uint32(screen), write_uint32(data1)],
    )


def LockStatusInfo(locked, method, strdata):
    log.info("-> LockStatusInfo")
    send_message(
        CoDiCommands.CMD_MTK_INFO_LOCK_STATUS,
        [write_uint16(locked), write_uint32(method), write_string(strdata)],
    )


def CallMuteStatusInfo(status):
    log.info("-> CallMuteStatusInfo")
    send_message(CoDiCommands.CMD_MTK_INFO_CALL_MUTE_STATUS, [write_uint32(status)])


def CallOutputInfo(output):
    log.info("-> CallOutputInfo")
    send_message(CoDiCommands.CMD_MTK_INFO_CALL_OUTPUT, [write_uint32(output)])


def CallOutputOptionsInfo(output_options):
    log.info("-> CallOutputOptionsInfo")
    send_message(
        CoDiCommands.CMD_MTK_INFO_CALL_OUTPUT_OPTIONS, [write_uint32(output_options)]
    )


def CameraStatusInfo(status):
    log.info("-> CameraStatusInfo")
    send_message(CoDiCommands.CMD_MTK_INFO_CAMERA_STATUS, [write_uint32(status)])


def CameraSettingsInfo(parameter, value):
    log.info("-> CameraSettingsInfo")
    send_message(
        CoDiCommands.CMD_MTK_INFO_CAMERA_SETTINGS,
        [write_uint32(parameter), write_uint32(value)],
    )


def VideoStatusInfo(status):
    log.info("-> VideoStatusInfo")
    send_message(CoDiCommands.CMD_MTK_INFO_VIDEO_STATUS, [write_uint32(status)])


def VideoSettingsInfo(parameter, value):
    log.info("-> VideoSettingsInfo")
    send_message(
        CoDiCommands.CMD_MTK_INFO_VIDEO_SETTINGS,
        [write_uint32(parameter), write_uint32(value)],
    )


def CoverLightSensorInfo(value):
    log.info("-> CoverLightSensorInfo")
    send_message(CoDiCommands.CMD_MTK_INFO_COVER_LIGHT_SENSOR, [write_uint32(value)])


def LoadLanguageResource(langid, resname, resdata, forcereload):
    log.info("-> LoadLanguageResource")
    send_message(
        CoDiCommands.CMD_MTK_LOAD_LANGUAGE_RESOURCE,
        [
            write_string(langid),
            write_string(resname),
            write_blob(resdata),
            write_uint32(forcereload),
        ],
    )


def GetCurrentLanguage():
    log.info("-> GetCurrentLanguage")
    send_message(CoDiCommands.CMD_MTK_GET_CURRENT_LANGUAGE)


def SetCurrentLanguage(langid):
    log.info("-> SetCurrentLanguage")
    send_message(CoDiCommands.CMD_MTK_SET_CURRENT_LANGUAGE, [write_string(langid)])


def ShowMedia(typestr, resname, seconds, speed, aftermode):
    log.info("-> ShowMedia")
    send_message(
        CoDiCommands.CMD_MTK_SHOW_MEDIA,
        [
            write_string(typestr),
            write_string(resname),
            write_uint32(seconds),
            write_uint32(speed),
            write_uint32(aftermode),
        ],
    )


def StopMedia(typestr, resname, aftermode):
    log.info("-> StopMedia")
    send_message(
        CoDiCommands.CMD_MTK_STOP_MEDIA,
        [write_string(typestr), write_string(resname), write_uint32(aftermode)],
    )


def LoadMedia(typestr, resname, resdata, loadmode):
    log.info("-> LoadMedia")
    send_message(
        CoDiCommands.CMD_MTK_LOAD_MEDIA,
        [
            write_string(typestr),
            write_string(resname),
            write_blob(resdata),
            write_uint32(loadmode),
        ],
    )


def UnloadMedia(typestr, resname):
    log.info("-> UnloadMedia")
    send_message(
        CoDiCommands.CMD_MTK_UNLOAD_MEDIA,
        [write_string(typestr), write_string(resname)],
    )


def HasMedia(typestr, resname):
    log.info("-> HasMedia")
    send_message(
        CoDiCommands.CMD_MTK_HAS_MEDIA, [write_string(typestr), write_string(resname)]
    )


def ShowAlert(
    alertmode,
    alertype,
    alerticondata,
    typestr,
    resname,
    seconds,
    speed,
    aftermode,
    option1,
    option2,
):
    log.info("-> ShowAlert")
    send_message(
        CoDiCommands.CMD_MTK_SHOW_ALERT,
        [
            write_uint32(alertmode),
            write_uint32(alertype),
            write_blob(alerticondata),
            write_string(typestr),
            write_string(resname),
            write_uint32(seconds),
            write_uint32(speed),
            write_uint32(aftermode),
            write_utf8_string(option1),
            write_utf8_string(option2),
        ],
    )


def StopAlert(aftermode):
    log.info("-> StopAlert")
    send_message(CoDiCommands.CMD_MTK_STOP_ALERT, [write_uint32(aftermode)])


def OrientationInfo(value):
    log.info("-> OrientationInfo")
    send_message(CoDiCommands.CMD_MTK_ORIENTATION_INFO, [write_uint32(value)])


def ActionCoDiHome(screenoff):
    log.info("-> ActionCoDiHome")
    send_message(CoDiCommands.CMD_MTK_ACTION_CODI_HOME, [write_uint32(screenoff)])


def NextAlarmInfo(appid, daystring, timestr):
    log.info("-> NextAlarmInfo")
    send_message(
        CoDiCommands.CMD_MTK_INFO_NEXT_ALARM,
        [write_uint32(appid), write_string(daystring), write_string(timestr)],
    )


def ShowBatteryLevel(percentage, showforseconds):
    log.info("-> ShowBatteryLevel")
    send_message(
        CoDiCommands.CMD_MTK_SHOW_BATTERY_LEVEL,
        [write_uint32(percentage), write_uint32(showforseconds)],
    )


def ContactInfo(contactid, totalcontacts, batchsize, contactname, msisdn):
    log.info("-> ContactInfo")
    send_message(
        CoDiCommands.CMD_MTK_CONTACT_INFO,
        [
            write_string(contactid),
            write_uint32(totalcontacts),
            write_uint32(batchsize),
            write_utf8_string(contactname),
            write_string(msisdn),
        ],
    )


def CallHistoryInfo(
    cdrid,
    totalcdr,
    batchsize,
    contactname,
    msisdn,
    day,
    month,
    year,
    hour,
    minute,
    second,
    tz,
    state,
):
    log.info("-> CallHistoryInfo")
    send_message(
        CoDiCommands.CMD_MTK_CALL_HISTORY_INFO,
        [
            write_uint32(cdrid),
            write_uint32(totalcdr),
            write_uint32(batchsize),
            write_utf8_string(contactname),
            write_string(msisdn),
            write_uint32(day),
            write_uint32(month),
            write_uint32(year),
            write_uint32(hour),
            write_uint32(minute),
            write_uint32(second),
            write_uint32(tz),
            write_uint32(state),
        ],
    )


def NotificationInfo(
    notid,
    action,
    appname,
    shortinfo,
    longinfo,
    day,
    month,
    year,
    hour,
    minute,
    second,
    tz,
    replyactions,
    replyaction1,
    replyaction2,
    replyaction3,
):
    log.info("-> NotificationInfo")
    send_message(
        CoDiCommands.CMD_MTK_NOTIFICATION_INFO,
        [
            write_uint32(notid),
            write_uint32(action),
            write_utf8_string(appname),
            write_utf8_string(shortinfo),
            write_utf8_string(longinfo),
            write_uint32(day),
            write_uint32(month),
            write_uint32(year),
            write_uint32(hour),
            write_uint32(minute),
            write_uint32(second),
            write_uint32(tz),
            write_uint32(replyactions),
            write_utf8_string(replyaction1),
            write_utf8_string(replyaction2),
            write_utf8_string(replyaction3),
        ],
    )


def PlayerInfo(appname, artist, album, track, offset, length, state, imageadr):
    log.info("-> PlayerInfo")
    send_message(
        CoDiCommands.CMD_MTK_PLAYER_INFO,
        [
            write_utf8_string(appname),
            write_utf8_string(artist),
            write_utf8_string(album),
            write_utf8_string(track),
            write_uint32(offset),
            write_uint32(length),
            write_uint32(state),
            write_blob(imageadr),
        ],
    )


def CallInfo(modem, action, contactid, contactname, msisdn, hasicon):
    log.info("-> CallInfo")
    send_message(
        CoDiCommands.CMD_MTK_CALL_INFO,
        [
            write_uint32(modem),
            write_uint32(action),
            write_string(contactid),
            write_utf8_string(contactname),
            write_string(msisdn),
            write_uint32(hasicon),
        ],
    )


def LEDisonModeInfo(value):
    log.info("-> LEDisonModeInfo")
    send_message(CoDiCommands.CMD_MTK_LEDISON_MODE_INFO, [write_uint32(value)])


def LEDisonPatternInfo(animid, animname, animationdata):
    log.info("-> LEDisonPatternInfo")
    send_message(
        CoDiCommands.CMD_MTK_LEDISON_PATTERN_INFO,
        [write_uint32(animid), write_utf8_string(animname), write_blob(animationdata)],
    )


def ContactIconInfo(contactid, contactname, msisdn, icondata):
    log.info("-> ContactIconInfo")
    send_message(
        CoDiCommands.CMD_MTK_CONTACT_ICON_INFO,
        [
            write_string(contactid),
            write_utf8_string(contactname),
            write_string(msisdn),
            write_blob(icondata),
        ],
    )


def ModemSignalInfo(sim1, sim2, sim2type):
    log.info("-> ModemSignalInfo")
    send_message(
        CoDiCommands.CMD_MTK_MODEM_SIGNAL_INFO,
        [write_uint32(sim1), write_uint32(sim2), write_uint32(sim2type)],
    )


def WeatherInfo(weatherstate, temp, scale, additionaltext):
    log.info("-> WeatherInfo")
    send_message(
        CoDiCommands.CMD_MTK_WEATHER_INFO,
        [
            write_uint32(weatherstate),
            write_uint32(temp),
            write_string(scale),
            write_string(additionaltext),
        ],
    )


def ExtraCommand(data1, data2, str1, str2):
    log.info("-> ExtraCommand")
    send_message(
        CoDiCommands.CMD_MTK_EXTRA_COMMAND,
        [
            write_uint32(data1),
            write_uint32(data2),
            write_string(str1),
            write_string(str2),
        ],
    )


def DateTimeFormat(dateformat, timeformat):
    log.info("-> DateTimeFormat")
    send_message(
        CoDiCommands.CMD_MTK_DATE_TIME_FORMAT_INFO,
        [write_string(dateformat), write_uint32(timeformat)],
    )


def AlbumArtInfo(albumartpng):
    log.info("-> AlbumArtInfo")
    send_message(CoDiCommands.CMD_MTK_ALBUM_ART_INFO, [write_blob(albumartpng)])


def CameraFrameImage(width, height, png):
    log.info("-> CameraFrameImage")
    send_message(
        CoDiCommands.CMD_MTK_CAMERA_FRAME_IMG,
        [write_uint16(width), write_uint16(height), write_blob(png)],
    )


def KeyPressInfo(keycode, mode, modifiers):
    log.info("-> KeyPressInfo")
    send_message(
        CoDiCommands.CMD_MTK_KEY_PRESS_INFO,
        [write_uint16(keycode), write_uint16(mode), write_uint16(modifiers)],
    )


def VoiceRecorderSettingsInfo(parameter, value):
    log.info("-> VoiceRecorderSettingsInfo")
    send_message(
        CoDiCommands.CMD_MTK_INFO_VOICE_RECODER_SETTINGS,
        [write_uint32(parameter), write_uint32(value)],
    )


def VoiceRecorderStatusInfo(status):
    log.info("-> VoiceRecorderStatusInfo")
    send_message(
        CoDiCommands.CMD_MTK_INFO_VOICE_RECORDER_STATUS, [write_uint32(status)]
    )


def MTKDataChangeAlert(type, data1):
    log.info("-> MTKDataChangeAlert")
    send_message(
        CoDiCommands.CMD_MTK_DATA_CHANGE_ALERT,
        [write_uint32(type), write_uint32(data1)],
    )


def SetMouse(onOff, absoluteOrRelative):
    log.info("-> SetMouse")
    send_message(146, [write_uint8(onOff), write_uint8(absoluteOrRelative)])
