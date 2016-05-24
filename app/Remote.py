from jsonRPC import jsonRPC
import cfg

class Remote(object):
	"""
	Controls the remote control command using json request
	"""
	def __init__(self,stbip):
		"""
		constructor
		@param stbip string Set top box's IP
		"""
		self.stbip = stbip
		self.url = "http://"+self.stbip+"/xxx?key={key}{hold}"

		self.keys = cfg.remote_keys

	
	def __process(self,key,hold=''):
		"""
		Generate the request to the box
		@param hold enum (keyPress,keyDown,keU) 
		@param key string defines the remote button used
		@returns bool the request was successful
		"""
		if (key in self.keys):
			json = jsonRPC()
			if len(hold)>0:
				hold = '&hold='+hold

			return json.request(self.url,{"key":key,"hold":hold})
		else:
			print "it's not a valid key"
			return False

###Public methods###
	def return_is_valid(self,msg,key,hold):
		"""
		Check if the return is valid comparing the data
		@param msg dict the return message from the request
		@param hold enum (keyPress,keyDown,keUp) 
		@param key string defines the remote button used
		@returns bool the request was successful
		"""
		if(hold==0):
			keyHold="keyPress"
		elif(hold==1):
			keyHold="keyDown"
		elif(hold==2):
			keyHold="keyUp"
		elif(hold==3):
			keyHold="keyPress"

		if type(msg)==dict:
			ok = msg['key']==key
			ok = ok and (msg['status']['code']==200)
			ok = ok and (msg['status']['msg']=="OK.")
			ok = ok and (msg['hold']==keyHold)
		else:
			ok = False

		return ok

	def send(self,hold,key):
		"""
		send a command to the box
		@param hold enum (0,1,2) represents Button Press Down or UP
		@param key string defines the remote button used
		@returns bool the request was successful
		"""
		if(hold==0): #Press
			ret = self.press(key)
		elif(hold==1): #Down
			ret = self.down(key)
		elif(hold==2): #Up
			ret = self.up(key)
		elif(hold==3): #None
			ret = self.__process(key)
		else:
			ret = None

		return ret

	def press(self,key):
		"""
		send a press command to the box
		@param key string defines the remote button used
		@returns bool the request was successful
		"""
		return self.__process(key,"keyPress")

	def up(self,key):
		"""
		send a up command to the box
		@param key string defines the remote button used
		@returns bool the request was successful
		"""
		return self.__process(key,"keyUp")

	def down(self,key):
		"""
		send a down command to the box
		@param key string defines the remote button used
		@returns bool the request was successful
		"""
		return self.__process(key,"keyDown")