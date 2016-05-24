from cfg import *
class MessageBox(object):
	"""
	Represents the message box
	"""
	def __init__(self,tipo='warning'):

		#: gtk.MESSAGE_INFO, gtk.MESSAGE_WARNING, gtk.MESSAGE_QUESTION or gtk.MESSAGE_ERROR.

		img = gtk.Image()
		_buttons = []
		if(tipo=="warning"):
			_tipo=gtk.MESSAGE_WARNING
			_buttons.append((gtk.STOCK_CLOSE,True))
			img.set_from_stock(gtk.STOCK_DIALOG_WARNING,5)
		elif(tipo=="info"):
			_tipo=gtk.MESSAGE_INFO
			_buttons.append((gtk.STOCK_CLOSE,True))
			img.set_from_stock(gtk.STOCK_DIALOG_INFO,5)
		elif(tipo=="question"):
			_tipo=gtk.MESSAGE_QUESTION
			_buttons.append((gtk.STOCK_YES,True))
			_buttons.append((gtk.STOCK_NO,False))
			img.set_from_stock(gtk.STOCK_DIALOG_QUESTION,5)
		elif(tipo=="error"):
			_tipo=gtk.MESSAGE_ERROR
			_buttons.append((gtk.STOCK_CLOSE,True))
			img.set_from_stock(gtk.STOCK_DIALOG_ERROR,5)
		else:
			_buttons.append((gtk.BUTTONS_OK,True))
			_buttons.append((gtk.BUTTONS_CANCEL,False))
			img.set_from_stock(gtk.STOCK_DIALOG_WARNING,5)


		self.msg = gtk.MessageDialog(flags=gtk.DIALOG_MODAL,type=_tipo)

		__buttons = []
		for i in _buttons:
			__buttons.append(self.msg.add_button(i[0],i[1]))

		__buttons[0].grab_default()

		self.msg.set_image(img)


	def mostrar(self,mensagem,msg2=''):
		"""
		Shows the alert screen
		"""

		self.msg.set_markup(mensagem)
		if(msg2!=''):
			self.msg.format_secondary_markup(msg2)

		self.msg.show_all()
		x =  self.msg.run()
		self.msg.destroy()
		return x