from jsonRPC import jsonRPC
from app.cfg import *


class Serial(object):
	"""
	Controls the serial command using json request
	"""

	def __init__(self, stbip):
		"""
		constructor
		@param stbip string Set top box's IP
		"""
		self.stbip = stbip
		self.url = "http://" + self.stbip + "/xxx?cmd={cmd}"

	def process(self,cmd):
		"""
		request the serial execution on the box
		@param cmd string command
		@returns bool the request was successful

		"""
		#if (cmd in self.cmds):
		json = jsonRPC()
		return json.request(self.url, {"cmd":cmd})
		#else:
		#print "it's not a valid command "+cmd
		#return False