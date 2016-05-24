from cfg import *
from func import *
from Remote import Remote
from Serial import Serial
from Window import Window
from auto import Auto
from gobject import timeout_add
from automate import Automate
from datetime import datetime
from MessageBox import MessageBox
from GenericView import GenericView
from Camera import Camera
from about import About
import threading


class Shef(Window):
	"""
	SHEF test Tool screen
	This class control the main view
	"""

	wdg="wdgSHEF"
	first_command = True

	def __init__(self):
		Window.show(self)
		
		wdg_retorno = self.get_wdg("txtRetorno")
		buffer = gtk.TextBuffer()
		wdg_retorno.set_buffer(buffer)
		
		tag_table = buffer.get_tag_table()

	        error_tag = gtk.TextTag("error")
        	error_tag.set_property("foreground", "red")
	        tag_table.add(error_tag)
		
		error_tag = gtk.TextTag("success")
        	error_tag.set_property("foreground", "blue")
	        tag_table.add(error_tag)

		default_tag = gtk.TextTag("default")
	        default_tag.set_property("foreground", "black")
	        tag_table.add(default_tag)

		self.stbip = []
		self.get_wdg('cbRemoteType').set_active(0)

		self.__fill_ip()
				
		self.__check_automate()
		WinCamera()


###Private methods###


	def __fill_ip(self):
		ip = get_arg(["--ip", "-i"])
		if ip is not None:
			
			if is_valid_ip(ip):
				store = gtk.ListStore(str)
				cbIP = self.get_wdg("cbIP")
				store.append([ip])
				cbIP.set_model(store)
				self.stbip.append(ip)
				cbIP.set_active(0)


	def __check_automate(self):
		arg = get_arg(['--auto', '-a'])
		if arg is not None:
			Automate(self)

	

	def __make_rem_readable(self, msg, tag="default"):
			
		message ="hold: " + msg['hold'] + "\n"
		message += "key: " + msg['key'] +"\n"
		message += "status: \n"
		message += "\tcode: " + str(msg['status']['code']) + "\n"
		message += "\tCommand Result: " + str(msg['status']['commandResult']) + "\n"
		message += "\tmsg: " + str(msg['status']['msg']) + "\n"
		message += "\tquery: " + str(msg['status']['query']) + "\n"

		return message


	def __make_serial_readable(self, cmd, msg):
		if cmd == "Active":
			pass
		elif cmd == "StandBy":
			pass

		return str(msg)

		
		
###Public methods###

	def show_message(self, msg, tag="default"):
		"""
		Shows a message on the blank area

		@param msg string the message to show
		@param tag enum(error,default, success)
		"""
		wdg_retorno = self.get_wdg("txtRetorno")

		buffer = wdg_retorno.get_buffer()
		#start = buffer.get_start_iter()
		end = buffer.get_end_iter()
		#buffer.delete(start,end)
		buffer.insert_with_tags_by_name(buffer.get_end_iter(), str(msg + "\n"), tag)
		end = buffer.get_end_iter()
		self.get_wdg('txtRetorno').scroll_to_iter(end, 0, False, 0.5, 0.5)


	def sendSerial(self,command):
		"""
		Prepare and send a serial command to Serial class

		@param cmd string command
		"""
		wdg_retorno = self.get_wdg("txtRetorno")
		if(self.first_command):
			self.first_command=False
			buffer = gtk.TextBuffer()
			wdg_retorno.set_buffer(buffer)

		command = self.get_wdg("cbSerialCommand").get_active_text()
		for ip in self.stbip:
			ser = Serial(ip)
			cmds = serial_commands[command]['serial']

			if (serial_commands[command]['complemento'] == False):
				retorno = ser.process(cmds)
				msg = "ip: %s\n"%(ip)
				self.show_message(msg + self.__make_serial_readable(command, retorno) + "\n")
			else:
				mb = MessageBox('error')
				mb.mostrar('Not implemented yet')

	def click_control(self, key, hold=None):
		ips = []
		cb = self.get_wdg("cbIP")
		model = cb.get_model()
		for ip in model:
			ips.append(ip[0])
		self.stbip = ips
		self.send(key, hold)

	def send(self, key, hold=None):
		"""
		Prepare, send and check return of a remote command to Remote class

		@param key string defines the remote button used
		@param hold enum (0,1,2) represents Button Press Down or UP
		@returns bool the request was successful and the return is valid
		"""
		if len(self.stbip) == 0:
			mb = MessageBox('error')
			mb.mostrar("Set an ip", "Please set an ip to send a command")
			return False

		for ip in self.stbip:
			wdg_retorno = self.get_wdg("txtRetorno")
			if(self.first_command):
				self.first_command = False
				
			if hold is None:
				hold = self.get_wdg("cbRemoteType").get_active()
			rem = Remote(ip)

			ret = rem.send(hold, key)
			msg = "ip: %s\n" % (ip)

			if ret is not None:
				if(rem.return_is_valid(ret, key, hold)):
					complete="Success!"
					tag = "success"
					
					self.show_message(msg + self.__make_rem_readable(ret) + "\n" + complete, tag)
				else:
					complete="Fail."
					tag = "error"
					self.stbip.remove(ip)
			else:
				complete = 'Fail.'
				tag = 'error'
				self.stbip.remove(ip)
				msg += "Timeout Connection\n"
				self.show_message(msg + complete, tag)


			
		
		return True if len(self.stbip) else False

	def add_ip(self):
		wdg = self.get_wdg("txtIP")
		ip = wdg.get_text()
		if is_valid_ip(ip):
			cb = self.get_wdg("cbIP")
			model = cb.get_model()
			model.append([ip])
			cb.set_model(model)
			cb.show()
			self.stbip.append(ip)
			if cb.get_active() == -1:
				cb.set_active(0)
		else:
			m = MessageBox('error')
			m.mostrar('Error', 'Invalid IP')
		wdg.set_text('')

	def h_btnAddIP(self, wdg):
		self.add_ip()

	def h_btnRemIP__clicked(self, wdg):
		cbIP = self.get_wdg("cbIP")
		ip = cbIP.get_active_text()
		if ip is not None:
			model = cbIP.get_model()			
			model.remove(cbIP.get_active_iter())
			cbIP.set_model(model)
			if self.stbip.count(ip) > 0:
				self.stbip.remove(ip)
			cbIP.show()

	def h_txtIP__key_press_event(self, wdg, event):
		enter = 65293 if sys.platform == 'win32' else 65421
		if event.keyval == enter:
			self.add_ip()

###Callbacks###

	def h_mnClear(self, wdg):
		wdg_retorno = self.get_wdg("txtRetorno")

		buffer = wdg_retorno.get_buffer()
		start = buffer.get_start_iter()
		end = buffer.get_end_iter()
		buffer.delete(start, end)

	def h_mnCamera(self, wdg):
		WinCamera()

	def h_mnSave(self, wdg):
		fd = gtk.FileChooserDialog(title=None, action=gtk.FILE_CHOOSER_ACTION_SAVE,
		buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
		fd.set_default_response(gtk.RESPONSE_OK)
		date_time = datetime.today()
		str_dt = str(date_time.year).zfill(4) + str(date_time.month).zfill(2) + str(date_time.day).zfill(2) + str(date_time.hour).zfill(2) + str(date_time.minute).zfill(2) + str(date_time.second).zfill(2)
		fd.set_current_name("shef_log_" + str_dt + ".log")
		response = fd.run()
		if response == gtk.RESPONSE_OK:
			filename = fd.get_filename()
	
			wdg_retorno = self.get_wdg("txtRetorno")
			buffer = wdg_retorno.get_buffer()
			start = buffer.get_start_iter()
			end = buffer.get_end_iter()

			content = buffer.get_text(start,end)
			f = open(filename,'w')
			f.write(content)
			f.close()

		fd.destroy()

	def h_mnOpenAutomate(self, wdg):
		a = Automate(self)
	
	def h_mnAbout(self, wdg):
		a = About()

	def h_mnClose(self, wdg):
		gtk.main_quit()
	
	def h_mnScriptSyntax(self, wdg):
		gv = GenericView()
		gv.show_script_syntax()

	def h_mnArguments(self, wdg):
		gv = GenericView()
		gv.show_command_line_args()


	def sair(self, widget):
		gtk.main_quit()



	def h_btnOK(self, wdg, a=None, b=None, c=None):
		ips = []
		cb = self.get_wdg("cbIP")
		model = cb.get_model()
		for ip in model:
			ips.append(ip[0])
		self.stbip = ips

	

###callback remote control###

	def h_btnPower(self, wdg):
		self.click_control("power")

	def h_btnPoweron(self, wdg):
		self.click_control("poweron")

	def h_btnPoweroff(self, wdg):
		self.click_control("poweroff")

	def h_btnFormat(self, wdg):
		self.click_control("format")

###callback trickplay###

	def h_btnPause(self, wdg):
		self.click_control("pause")

	def h_btnRew(self, wdg):
		self.click_control("rew")

	def h_btnReplay(self, wdg):
		self.click_control("replay")

	def h_btnStop(self, wdg):
		self.click_control("stop")

	def h_btnAdvance(self, wdg):
		self.click_control("advance")

	def h_btnFfwd(self, wdg):
		self.click_control("ffwd")

	def h_btnRecord(self, wdg):
		self.click_control("record")

	def h_btnPlay(self, wdg):
		self.click_control("play")

###callback navigation###
	
	def h_btnGuide(self, wdg):
		self.click_control("guide")

	def h_btnActive(self, wdg):
		self.click_control("active")

	def h_btnList(self, wdg):
		self.click_control("list")

	def h_btnExit(self, wdg):
		self.click_control("exit")

	def h_btnUp(self, wdg):
		self.click_control("up")

	def h_btnRight(self, wdg):
		self.click_control("right")

	def h_btnDown(self, wdg):
		self.click_control("down")

	def h_btnLeft(self, wdg):
		self.click_control("left")

	def h_btnSelect(self, wdg):
		self.click_control("select")

	def h_btnBack(self, wdg):
		self.click_control("back")

	def h_btnMenu(self, wdg):
		self.click_control("menu")

	def h_btnInfo(self, wdg):
		self.click_control("info")

	def h_btnRed(self, wdg):
		self.click_control("red")

	def h_btnGreen(self, wdg):
		self.click_control("green")

	def h_btnYellow(self, wdg):
		self.click_control("yellow")

	def h_btnBlue(self, wdg):
		self.click_control("blue")

###callback tv control###

	def h_btnChanup(self, wdg):
		self.click_control("chanup")

	def h_btnChandown(self, wdg):
		self.click_control("chandown")

	def h_btnMute(self, wdg):
		self.click_control("mute")

	def h_btnPrev(self, wdg):
		self.click_control("prev")

###callback numeric###

	def h_btn0(self, wdg):
		self.click_control("0")

	def h_btn1(self, wdg):
		self.click_control("1")

	def h_btn2(self, wdg):
		self.click_control("2")

	def h_btn3(self, wdg):
		self.click_control("3")

	def h_btn4(self, wdg):
		self.click_control("4")

	def h_btn5(self, wdg):
		self.click_control("5")

	def h_btn6(self, wdg):
		self.click_control("6")

	def h_btn7(self, wdg):
		self.click_control("7")

	def h_btn8(self, wdg):
		self.click_control("8")

	def h_btn9(self, wdg):
		self.click_control("9")

	def h_btnDash(self, wdg):
		self.click_control("dash")

	def h_btnEnter(self, wdg):
		self.click_control("enter")


class WinCamera(Window):

    def __init__(self): 
        self.wdg = 'wdgCamera'
        self.threads = []
        Window.show(self)
        img = self.get_wdg('imgCamera')
        self.update = UpdateImg(img)
        self.update.start()

    def h_btnCapture__clicked(self, wdg):
        camera = Camera.get_instance()
        name = 'snapshot/' + str(time.time()) + '.jpg'
        camera.save_frame(name)

    def sair(self, blank=None):
        self.update.join()

class UpdateImg(object):
    def __init__(self, img):
        self.img = img        
        self.quit = False
        self.camera = Camera.get_instance()
        #super(UpdateImg, self).__init__()
        self.stoprequest = False
        
    def start(self):
    	self.stoprequest = False
    	self.run()

    def update_img(self):
        image_rgb = self.camera.get_image()
        if image_rgb is None:
            return
        pixbuf = gtk.gdk.pixbuf_new_from_data(image_rgb.tostring(), gtk.gdk.COLORSPACE_RGB, False, image_rgb.depth, image_rgb.width/3*2, image_rgb.height/3*2, image_rgb.width*image_rgb.nChannels)            
        self.img.set_from_pixbuf(pixbuf)
        return

    def run(self):   
        if not self.stoprequest:
            self.update_img()
            timeout_add(10, self.run)

    def join(self, timeout=None):
        self.stoprequest=True
        #super(UpdateImg, self).join(timeout)
            
"""
class UpdateImg(threading.Thread):
    def __init__(self, img):
        self.img = img        
        self.quit = False
        self.camera = Camera.get_instance()
        super(UpdateImg, self).__init__()
        self.stoprequest = threading.Event()
        
    def update_img(self):
        image_rgb = self.camera.get_image()
        if image_rgb is None:
            return
        pixbuf = gtk.gdk.pixbuf_new_from_data(image_rgb.tostring(), gtk.gdk.COLORSPACE_RGB, False, image_rgb.depth, image_rgb.width, image_rgb.height, image_rgb.width*image_rgb.nChannels)            
        self.img.set_from_pixbuf(pixbuf)
        return

    def run(self):   
        while not self.stoprequest.isSet():
            gobject.idle_add(self.update_img)
            time.sleep(0.1)

    def join(self, timeout=None):
        self.stoprequest.set()
        #super(UpdateImg, self).join(timeout)
"""