from gi.repository import GLib
from pydbus import SystemBus, SessionBus
import logging
import codi_mtk_generated_functions as mtk_cmd
import led_manager
import property_manager

log = logging.getLogger("codi-app: ({})".format(__name__))


def addressbookChanged(par1, par2, par3, par4, par5):
    print("AddressBook Changed")
    mtk_cmd.MTKDataChangeAlert(1, 0)
    mtk_cmd.MTKDataChangeAlert(0, 0)


def init(startMainLoop=True):
    global bus
    global session
    global ril0
    global ril1
    global power
    global network

    bus = SystemBus()
    #  bus.subscribe(signal_fired=print)
    power = bus.get(".UPower")
    power.onPropertiesChanged = property_manager.propertiesChanged
    power = bus.get(".UPower", "/org/freedesktop/UPower/devices/battery_battery")
    power.onPropertiesChanged = property_manager.propertiesChanged
    led_manager.ledsCharging(power.State == 1)

    ril0 = bus.get("org.ofono", "/ril_0")
    ril0.onCallAdded = property_manager.callStatusChanged
    ril0.onCallRemoved = property_manager.callStatusChanged
    ril1 = bus.get("org.ofono", "/ril_1")
    ril1.onCallAdded = property_manager.callStatusChanged
    ril1.onCallRemoved = property_manager.callStatusChanged

    network = bus.get("org.freedesktop.NetworkManager")
    network.onPropertiesChanged = property_manager.networkPropertiesChanged
    mtk_cmd.WiFiStatusInfo(int(network.WirelessEnabled), 100)

    property_manager.init()

    session = SessionBus()
    session.subscribe(
        object="/com/canonical/pim/AddressBook", signal_fired=addressbookChanged
    )

    # help(ril0)
    # ril0['org.ofono.CallVolume'].onPropertyChanged = propertyChanged

    # ril0['org.ofono.VoiceCallManager'].onPropertyChanged = propertyChanged
    # print(dir(ril0['org.ofono.VoiceCallManager']))
    # notifications = session.get('org.kde.kglobalaccel', '/component/kmix')
    # notifications.onglobalShortcutPressed = volumeChanged

    if startMainLoop:
        loop = GLib.MainLoop()
        loop.run()
