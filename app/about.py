from cfg import *

from app.Window import Window

class About(Window):
	wdg = 'wdgAbout'

	def __init__(self):
		self.show()

	def h_btnClose(self,wdg):
		self.window.destroy()