from cfg import *
import os
from app.Window import Window
from app.auto import Auto

class Automate(Window):
	"""
	Controls the view to run automation scripts
	"""
	wdg="wdgAutomate"

	def __init__(self,interface):
		#ler a pasta scripts
		#montar a combo com os arquivos .shef
		self.show()
		
		self.__fill_combo()

		self.auto = Auto(interface)		
		self.auto.add_observer(self)
		#auto load script

		
		self.__sensitive(False)
		self.__check_args()

###Private methods###

	def __fill_combo(self):
		folder_content = os.listdir("./scripts")
		store = gtk.ListStore(str)
		cb = self.get_wdg("cbFileChoose")
		
		for item in folder_content:
			if item[-5:] == ".shef":
				store.append([item])

		cell = gtk.CellRendererText()
	        cb.pack_start(cell, True)
	        cb.add_attribute(cell, 'text', 0)
		cb.set_model(store)
		cb.set_active(0)

	def __sensitive(self, sen):
		self.get_wdg("btnPrevious").set_sensitive(sen)
		self.get_wdg("btnNext").set_sensitive(sen)
		self.get_wdg("btnStopExec").set_sensitive(sen)
		self.get_wdg("btnPlayExec").set_sensitive(sen)
		self.get_wdg("btnExec").set_sensitive(sen)
	

	def __check_args(self):
		"""
		Define startup parameters.
		--auto [script] or -a [script] autoselect a scriptfile named [script]
		--start or -s play the script loaded automactaly
		"""
		arg = get_arg(['--auto', '-a'])
		if arg != None:
			self.__load_script(arg)
			cb = self.get_wdg('cbFileChoose')
			try:
				cb.set_active(0)
				m = cb.get_model()
			
				for item in m:
					if item[0] == arg:
						cb.set_active_iter(item.iter)
						break
			except:
				cb.set_active(0)

		arg = get_arg(['--start', '-s'])
		if arg is not None:
			self.get_wdg("btnPlayExec").set_active(True)
			self.auto.play()
			
			

	def __load_script(self, filename):
		"""
		Load the script file
		"""
		if self.auto.load_script(filename):
			self.get_wdg("lbLineStr").set_text("Script loaded successfully.")

		        self.get_wdg("pbAutomate").set_fraction(0.0)
		        self.get_wdg("pbAutomate").set_orientation(gtk.PROGRESS_LEFT_TO_RIGHT)
			return True
		else:
			self.get_wdg("lbLineStr").set_text("File not detected.")
			return False
		
###Callback methods###

	def h_cbFileChoose(self, wdg):
		self.__sensitive(False)
		
	def h_btnOpenFile(self, wdg):
		selected = self.get_wdg("cbFileChoose").get_active_text()
		if self.__load_script(selected):
			self.__sensitive(True)

	def h_btnPrevious(self, wdg):
		self.get_wdg("btnPlayExec").set_active(False)
		self.auto.previous()
		self.update_data()

	def h_btnNext(self, wdg):
		self.get_wdg("btnPlayExec").set_active(False)
		self.auto.next()
		self.update_data()

	def h_btnStopExec(self, wdg):
		self.get_wdg("btnPlayExec").set_active(False)
		self.auto.pause()
		self.auto.reset()
		self.get_wdg("pbAutomate").set_fraction(0.0)
		self.update_data()
	
	def h_btnExec(self, wdg):
		self.auto.play()
		self.auto.pause()
		self.update_data()

	def h_btnPlayExec(self, wdg):
		if self.get_wdg("btnPlayExec").get_active():
			self.auto.play()
		else:
			self.auto.pause()

		self.update_data()

###Public methods###
	def update_data(self):
		n = self.auto.getLineNumber()
		t = self.auto.getQtdeLines()

		c = self.auto.getLineContent()
		if c[0] != "#":
			c = c.strip().split("\t")
			time = c[0]
			shift = 0

			cmd = c[1]

			if len(c) == 3:
				key = c[2]
			else:
				key = None

			if cmd == "msg":
				msg = "Just showing a message"
			elif cmd == 'snapshot':
				msg = 'Taking a Snapshot'
			else:
				msg = "Sending button " + key + " " + cmd
			
			if float(time) < 0:
				msg +=" and waiting a click"
			elif cmd != 'snapshot':
				msg +=" and waiting " + time + " seconds"
	
			self.get_wdg("lbLineStr").set_text(msg)

			self.get_wdg("lbLineNumber").set_text("  Line " + str(n + 1) + "/" + str(t))


			self.get_wdg("pbAutomate").set_fraction((n + 1.0) / t)




	def signal(self,auto,msg):
		if msg == 'step':
			self.update_data()
		elif msg == "stop":
			self.h_btnStopExec('')