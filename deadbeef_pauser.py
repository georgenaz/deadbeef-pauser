#!/usr/bin/env python2.7

import glib, gobject
gobject.threads_init()

import dbus, os

SERVICES = [
    dict( # GNOME
        bus_name='org.gnome.ScreenSaver',
        path='/org/gnome/ScreenSaver',
        dbus_interface='org.gnome.ScreenSaver',
    ),
    dict( # KDE
        bus_name='org.freedesktop.ScreenSaver',
        path='/',
        dbus_interface='org.freedesktop.ScreenSaver',
    ),
]

def screensaver_active_changed( is_active ):
    if is_active:
        os.system('if [[ `pidof deadbeef` ]]; then deadbeef --pause 2>/dev/null; fi')


import dbus.mainloop.glib as dbgl
dbgl.DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()

for service in SERVICES:
    try:
        proxy = bus.get_object( service['bus_name'], service['path'],
            follow_name_owner_changes=True )
    except dbus.DBusException:
        continue
    break

assert proxy
interface = dbus.Interface( proxy, service['dbus_interface'] )
mainloop = glib.MainLoop()

interface.connect_to_signal( 'ActiveChanged', screensaver_active_changed )

# For some reason Lock never returns.
interface.Lock( ignore_reply=True )

mainloop.run()

