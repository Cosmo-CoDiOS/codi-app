import logging
import dbus
import vobject
from codi_server import CodiStatus

log = logging.getLogger("codi: ({})".format(__name__))


def contact_name_for_number(number) -> str:
    for c in CodiStatus.Contacts:
        if c[2] == number:
            return c[1]
    return "Unknown"


def get_contacts_from_dbus():
    addressbook_uid = "system-address-book"

    CodiStatus.Contacts = []

    # add dbus-attr
    try:
        # load bus
        bus = dbus.SessionBus()

        proxy = bus.get_object("org.freedesktop.DBus", "/")
        interface = dbus.Interface(proxy, "org.freedesktop.DBus")

        EDS_FACTORY_BUS = list(
            filter(
                lambda x: "org.gnome.evolution.dataserver.AddressBook" in x,
                interface.ListActivatableNames(),
            )
        )[0]

        interface = dbus.Interface(
            bus.get_object(
                EDS_FACTORY_BUS, "/org/gnome/evolution/dataserver/AddressBookFactory"
            ),
            "org.gnome.evolution.dataserver.AddressBookFactory",
        )

        EDS_SUBPROCESS_OBJ_PATH, EDS_SUBPROCESS_BUS = interface.OpenAddressBook(
            addressbook_uid
        )

        proxy = bus.get_object(EDS_SUBPROCESS_BUS, EDS_SUBPROCESS_OBJ_PATH)
        interface = dbus.Interface(proxy, "org.gnome.evolution.dataserver.AddressBook")

        contacts = interface.GetContactListUids("")

        for uid in contacts:
            raw_contact = interface.GetContact(uid)
            vcard = vobject.readOne(raw_contact)
            # check for name and telephone
            # we need this!
            try:
                if vcard.tel_list is None and vcard.fn is None:
                    continue
            except KeyError:
                continue
            # check for uid
            if vcard.uid is None:
                continue  # no uid, skip this entry
                # this would tend to be a malformed contact, so we're not
                # missing anything here

            # code derived from PC (Davide) - check for deleted entry
            try:
                if vcard.contents.get("X-DELETED-AT"):
                    # deleted, don't sync to CoDi
                    continue
            except KeyError:
                continue

            name = vcard.fn
            uid = vcard.uid
            nums = []

            for tel in vcard.tel_list:
                try:
                    # check for tel value and type
                    # then add to list
                    if tel.params["TYPE"][0] is not None:
                        nums += [(tel.params["TYPE"][0], tel.value)]
                    elif tel.params["TYPE"][0]:
                        # type is empty, result to default
                        nums += [("Default", tel.value)]
                    else:
                        # value and/or tel type doesn't exist - skip entry
                        continue
                except KeyError:
                    # this is unexpected.
                    continue

            for n in nums:
                CodiStatus.Contacts += [(uid, name, n[1])]

        print(CodiStatus.Contacts)
    except Exception as e:
        log.error("Exception: %r", e)
