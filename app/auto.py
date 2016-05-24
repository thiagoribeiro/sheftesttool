import os.path
import cfg
import datetime
import time
from MessageBox import MessageBox
from Camera import Camera
from gobject import timeout_add, source_remove

class Auto(object):
	"""
	Controls the execution of the automation scripts
	"""
	def __init__(self, interface):
		self.interface = interface
		self.play_cmd = False
		self.observers = []
		self.scripts = ""
		self.script = None
		self.line_number=0

###Private methods###
	def show_message(self, msg, tag='default', line=None):
		date_time = datetime.datetime.today()
		momment = "[" + str(date_time.hour).zfill(2) + ":" + str(date_time.minute).zfill(2) + ":" + str(date_time.second).zfill(2) + "]" 
		
		if line is not None:
			msg += " on line " + str(line)

		self.interface.show_message(momment + "------------------------------------------------", tag)
		self.interface.show_message(momment + " " + msg, tag)
		

	def message(self, msg, time):
		"""
		Execute the msg command in the script showing the message on the blank screen
		"""
		self.show_message("MSG: " + msg, 'success')
		self.wait(time)

	def execute(self, command, key, time, comment=''):
		"""
		Execute a Remote command in the script 
		"""
		if len(comment) > 0:
			comment = "     #  " + comment
		self.show_message(command + " " + key + comment)
		hold = {"press":0, "down":1, "up":2, "none":3}[command]
		ret = self.interface.send(key, hold)
		self.wait(time)
		return ret

	def wait(self, sec_time):
		"""
		Sets the waiting time_ after run the command line
		"""
		self.sec_time = float(sec_time)


	def wait_exec(self):
		"""
		Really wait for the time_ defined or by a click on the box
		"""
		sec_time = self.sec_time

		if sec_time < 0:
			self.show_message("Waiting a click")
			m = MessageBox('info')
			m.mostrar('Wait Box','Click to continue')
			self.next_step = timeout_add(50, self.step)

		else:
			self.show_message("Waiting ddd "+ str(sec_time) + " seconds")
			self.next_step = timeout_add(int(sec_time * 1000), self.step)


	def parse(self, line, comment=""):
		"""
		Parses the script line and prepare it to be executed
		"""
		commands = ("press", "down", "up", "none", "msg", 'snapshot')
		shift = 0
		time_ = -1
		line = line.strip().lower().split("\t")
		#time_: wait time_ in seconds after exec | -1 to wait dialog (default)
		#command: press or down or up or msg
		#if command!=msg
		#	key: remote key
		#else
		#	message
		if line[0] in commands:
			command = line[0].strip()
		elif line[1] in commands:
			shift=1
			command = line[1].strip()
			if(line[0].replace("-", "").replace('.', '').isdigit()):
				time_ = line[0].strip()
			else:
				self.show_message(line[0].strip() + " is not a valid number", 'error', self.line_number)
				self.warn_observers('stop')


		if command == "msg":
			msg = line[shift + 1].strip()
			self.message(msg, time_)
			ret = True
		elif command == 'snapshot':
			self.snapshot()
			ret = True
		else:
			key = line[shift + 1].strip()

			if key in cfg.remote_keys:
				ret = self.execute(command, key, time_, comment)
			else:
				ret = False
				self.show_message("Undefined key " + key, 'error', self.line_number)
				self.warn_observers('stop')
		return ret

	def warn_observers(self, msg):
		"""
		Warn the observers about a new line execution
		"""
		for obj in self.observers:
			obj.signal(self, msg)

###Public methods###
		
	def step(self):
		"""
		Execute the script line by line
		"""
		if not self.play_cmd:
			return False		
		
		line = self.get()
		self.warn_observers('step')
		if(line):
			if line[0]!='#':
				line = line.split('#')

				comment = ""
				if len(line) > 1:
					comment = line[1]
					
				line = line[0]
				if self.parse(line, comment):
					self.wait_exec()
				else:
					self.show_message("Stopped! Box returns error", 'error', self.line_number)
					self.warn_observers('stop')					
			else:
				self.show_message("#     " + line[1:])
				self.step()
		else:
			self.show_message("End.")
			m = MessageBox('info')
			m.mostrar('Process Finished', '')
			self.warn_observers('stop')


	def load_script(self, filename):
		"""
		Load content of the script file
		"""
		self.script = filename
		if(os.path.exists('./scripts/' + filename)):
			f= open('./scripts/' + filename, 'r')
			self.scripts = f.readlines()

			i=0
			for line in self.scripts:
				if len(line.strip()) == 0:
					del(self.scripts[i])
					i -= 1
				i += 1

			f.close()
			self.reset()
			return True
		else:
			self.show_message("File not exists", 'error')			
			return False

	def getQtdeLines(self):
		return len(self.scripts)
	
	def getLineNumber(self):
		return self.line_number - 1
	
	def getLineContent(self):
		if self.line_number < 1 or len(self.scripts) < self.line_number:
			line = self.scripts[0]
		else:
			line = self.scripts[self.line_number - 1]

		return line


	def run_script(self):
		"""
		Execute  the script
		"""
		self.pause()
		self.reset()
		#executar as acoes do arquivo
		self.play()


	def next(self):
		"""
		Change current line to the next one
		"""
		if len(self.scripts) > self.line_number + 1:
			self.line_number += 1
			if self.scripts[self.line_number][0] == '#':
				self.next()

	def previous(self):
		"""
		Change current line to the previous one
		"""
		if self.line_number > 0:
			self.line_number -= 1

			if self.scripts[self.line_number][0] == '#':
				self.previous()
		else:
			if self.scripts[self.line_number][0] == '#':
				self.next()

	def get(self):
		"""
		Return the current line
		"""
		if len(self.scripts) > self.line_number:
			self.line_number += 1
			return self.scripts[self.line_number - 1]
		else:
			return None

	def reset(self):
		self.line_number = 0
	
	def play(self):
		"""
		Start the automatic execution
		"""
		self.show_message("Starting process from line " + str(self.line_number) + ".")
		self.play_cmd = True
		self.step()

	def pause(self):
		"""
		Pause the automatic execution
		"""
		self.show_message("Process paused on line " + str(self.line_number) + ".")
		self.play_cmd = False
		try:
			source_remove(self.next_step)
		except:
			pass

	def add_observer(self, obj):
		"""
		Add an observer to be signaled about a new line execution
		"""
		self.observers.append(obj)

	def snapshot(self):
		camera = Camera.get_instance()
		pos = self.script.find('.shef')
		path = 'log/' + self.script[0:pos] + '/'
	        if not os.path.exists(path):
		    os.mkdir(path)
		name = path + str(time.time()) + '.jpg'
		camera.save_frame(name)