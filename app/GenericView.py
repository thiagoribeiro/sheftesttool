from cfg import *
from Window import Window


class GenericView(Window):
	"""
	Screen to show information
	"""

	wdg="wdgGenericView"
	first_command=True

	def __init__(self,title=''):
		Window.show(self)
		
		wdg_retorno = self.get_wdg("txtGenericContent")
		buffer = gtk.TextBuffer()
		wdg_retorno.set_buffer(buffer)
		
		tag_table = buffer.get_tag_table()

	        tag = gtk.TextTag("title")
        	tag.set_property("foreground", "brown")
		tag.set_property("size",14000)
		tag.set_property("weight",100)

	        tag_table.add(tag)

		
		tag = gtk.TextTag("text")
		tag.set_property("foreground", "black")
		tag.set_property("size",11000)
		tag.set_property("weight",60)

		tag_table.add(tag)
		
		self.window.set_title(title)
	
	def clear(self):
		"""
		Clear the blank screen
		"""
		wdg_retorno = self.get_wdg("txtGenericContent")

		buffer = wdg_retorno.get_buffer()
		start = buffer.get_start_iter()
		end = buffer.get_end_iter()
		buffer.delete(start,end)

	def show_message(self,msg,tag="text"):
		"""
		Shows a message on the blank area

		@param msg string the message to show
		@param tag enum(title,text)
		"""
		wdg_retorno = self.get_wdg("txtGenericContent")

		buffer = wdg_retorno.get_buffer()
		end = buffer.get_end_iter()
		buffer.insert_with_tags_by_name(buffer.get_end_iter(), str(msg+"\n"), tag)

	
	def show_script_syntax(self):
		self.window.set_title('Shef Automate Script Syntax')
		arq = open('help/syntax.shef')
		lines = arq.readlines()
		for line in lines:
			line = line.split('/#')
			text = line[0].replace("\n", '')
			format = 'text'
			if len(line) > 1:
				format = line[1].strip()
			self.show_message(text, format)
		arq.close()
		

	def show_command_line_args(self):
		self.window.set_title('Command line Arguments')
		arq = open('help/command.shef')
		lines = arq.readlines()
		for line in lines:
			line = line.split('/#')
			text = line[0].replace("\n", '')
			format = 'text'
			if len(line) > 1:
				format = line[1].strip()
			self.show_message(text, format)
		arq.close()

	
	def h_gvClose(self,wdg):
		self.window.destroy()