#
# Gtk 2/3 compat package
# Copyright (c) 2017 Red Hat, Inc.  Distributed under GPLv2.
#

try: # python2 / gtk2 / pygtk
    import gtk
    import gtk.glade
    import gobject

    gtk.glade.bindtextdomain("rhn-client-tools", "/usr/share/locale")
    GTK3 = False
except ImportError: # python3 /gtk3 / gi
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk as gtk
    from gi.repository import GObject as gobject
    GTK3 = True


if GTK3:
    class GladeBuilder(object):
        def __init__(self):
            self.builder = gtk.Builder()
            self.builder.get_widget = self.builder.get_object
            self.builder.signal_autoconnect = self.builder.connect_signals
            self.translation_domain = None

        def XML(self, gladefile, widget, domain):
            self.builder.add_objects_from_file(gladefile, (widget,))
            if not self.translation_domain:
                self.builder.set_translation_domain(domain)
            return self.builder

    gtk.glade = GladeBuilder()
    gtk.RESPONSE_NONE = gtk.ResponseType.NONE

    def getWidgetName(widget):
        return gtk.Buildable.get_name(widget)

else:
    def getWidgetName(widget):
        return widget.name