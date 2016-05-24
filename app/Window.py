try:
    import pygtk
    pygtk.require("2.0")
except:
	pass
try:
	import gtk
	import gtk.glade
except:
	print "GTK not detected"

import cfg

class Window(object):
	"""
	Represents a graphic window view abstraction
	"""
	wdg = ""
	def get_wdg(self,wdg):
		return self.glade.get_widget(wdg)

	def sair(self, blank=None):
		pass

	def show(self):
		self.glade = gtk.glade.XML(cfg.gladefile, self.wdg)
		self.window = self.glade.get_widget(self.wdg)
		#gtk.gdk.Cursor(gtk.gdk.LEFT_PTR)

		self.window.show()
		self.glade.signal_autoconnect(self)
		self.window.connect('destroy', self.sair)

