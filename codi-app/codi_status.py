import logging

log = logging.getLogger("codi-app: ({})".format(__name__))


class CallInfo:
    modem_id: int = 0
    contact_name: str = ""
    ms_isdn: str = ""
    currentCall: bool = False
    state: str = ""

    def __init__(self):
        pass


class DeviceInfo:
    battery_level: int = 0
    # by default, we assume the Cosmo is open upon Gemian boot, and thus upon codi-app start.
    lid_closed: bool = False

    def __init__(self):
        pass


class CoDiProtocol:
    major_version: int = 0
    minor_version: int = 0

    def __init__(self, major: int, minor: int):
        self.major_version = major
        self.minor_version = minor


class CoDiInfo:
    codi_protocol: CoDiProtocol
    codi_version: str = ""
    codi_resources_version: str = ""

    def __init__(self):
        pass


class CoDiStatus:
    call_info: CallInfo = CallInfo()
    device_info: DeviceInfo = DeviceInfo()
    contacts: list = []
    info: CoDiInfo = CoDiInfo()

    def __init__(self):
        try:
            with open("/proc/battery_status") as f:
                self.device_info.battery_level = int(f.read().split(",")[1])
        except Exception as e:
            log.error(e)
