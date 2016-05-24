##TODO: Automatic scroll
##TODO: Stop exec on ESC


from app.cfg import *
from app.interface import Shef
from app.AutomateCommandLine import AutomateCommandLine

if sys.platform == 'win32':
    import win32api, win32con


#Everything starts here
if __name__ == "__main__":
	
    

    options, args = parser.parse_args()
    if options.commandline: 
        a = AutomateCommandLine(options.ip, options.queue, args[0])
        a.close_files()
    else:
        path = os.path.abspath('.')
        gtkrc = path + '\\tema\\MurrinaAquaIsh\\gtkrc'
        gtk.rc_set_default_files([gtkrc])
        gtk.rc_reparse_all_for_settings(gtk.settings_get_default(), True)
        #gtk.gdk.threads_init()
        s = Shef()
        #gtk.gdk.threads_enter()
        gtk.main()
        #gtk.gdk.threads_leave()

if sys.platform == 'win32': #Kamikaze
    handle = win32api.OpenProcess( win32con.PROCESS_TERMINATE, 0, os.getpid() )
    win32api.TerminateProcess( handle, 0 )
    win32api.CloseHandle( handle )