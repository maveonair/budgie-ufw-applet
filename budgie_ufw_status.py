#!/usr/bin/env python3

# Copyright (C) 2020 Fabian Mettler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import configparser
import threading
import time

import gi.repository
gi.require_version('Budgie', '1.0')
from gi.repository import Budgie, GObject, Gtk, GLib


class BudgieUfwStatus(GObject.GObject, Budgie.Plugin):
    __gtype_name__ = "BudgieUfwStatus"

    def __init__(self):
        GObject.Object.__init__(self)

    def do_get_panel_widget(self, uuid):
        return BudgieUfwStatusApplet(uuid)


class BudgieUfwStatusApplet(Budgie.Applet):
    img = None

    def __init__(self, uuid):
        Budgie.Applet.__init__(self)

        self.img = Gtk.Image.new_from_icon_name("firewall-applet", Gtk.IconSize.BUTTON)

        def background_check():
            while True:
                GLib.idle_add(self.update_icon)
                time.sleep(5)

        self.update_icon()
        self.add(self.img)
        self.show_all()

        thread = threading.Thread(target=background_check)
        thread.daemon = True
        thread.start()

    def ufw_is_enabled(self):
        config = self.ufw_config()
        return config['UFW']['ENABLED'] == 'yes'


    def ufw_config(self):
        with open('/etc/ufw/ufw.conf', 'r') as f:
            config_string = '[UFW]\n' + f.read()

        config = configparser.ConfigParser()
        config.read_string(config_string)
        return config

    def update_icon(self):
        if self.ufw_is_enabled():
            self.img.set_from_icon_name("firewall-applet", Gtk.IconSize.BUTTON)
        else:
            self.img.set_from_icon_name("firewall-applet-panic", Gtk.IconSize.BUTTON)
