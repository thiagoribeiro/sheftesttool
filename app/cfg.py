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

import sys
import time
import os
import datetime
import getopt
import gobject
from optparse import OptionParser


use = "Usage: %prog [options] argument1"

parser = OptionParser(usage=use)

parser.add_option("-c", "--commandline", dest="commandline", action="store_true", default=False)
parser.add_option("-i", "--ip", dest="ip", metavar="ip")
parser.add_option("-q", "--queue", dest="queue", metavar="queue")



### The glade file
gladefile = "glade/interface.glade"

### Acceptable remote keys
remote_keys =  ['enter','dash','0','1','2','3','4','5','6','7','8','9','guide','active','list','exit','up','right','down','left','select','back','menu','info','red','green','yellow','blue','chanup','chandown','prev','pause','rew','replay','stop','advance','ffwd','record','play','power','poweron','poweroff','format']

### Acceptabie serial commands
serial_coxxxxds={}
serial_coxxxxds['Active'] = {"serial":"xxxx", "complemento":False}
serial_coxxxxds['Standby'] = {"serial":"xxxx", "complemento":False}
serial_coxxxxds['SendUserCommand'] = {"serial":"xxxx","complemento":True}
serial_coxxxxds['GetReturnValue'] = {"serial":"xxxx","complemento":False}
serial_coxxxxds['GetCurrentTime'] = {"serial":"xxxx","complemento":False}
serial_coxxxxds['GetUserCommand'] = {"serial":"xxxx","complemento":False}
serial_coxxxxds['GetCurrentChannel'] = {"serial":"xxxx","complemento":False}
serial_coxxxxds['GetCurrentChannelMT'] = {"serial":"xxxx","complemento":True}
serial_coxxxxds['GetCommandVersion'] = {"serial":"xxxx","complemento":False}
serial_coxxxxds['GetPrimaryStatus'] = {"serial":"xxxx","complemento":False}
serial_coxxxxds['GetPrimaryStatusMT'] = {"serial":"xxxx","complemento":True}
serial_coxxxxds['GetSignalQuality'] = {"serial":"xxxx","complemento":True}
serial_coxxxxds['GetSignalQualityMT'] = {"serial":"xxxx","complemento":True}
serial_coxxxxds['OpenUserChannel'] = {"serial":"xxxx","complemento":True}
serial_coxxxxds['OpenUserChannelMT'] = {"serial":"xxxx","complemento":True}
serial_coxxxxds['GetTuner'] = {"serial":"xxxx","complemento":False}
serial_coxxxxds['DisableUserEntry'] = {"serial":"xxxx","complemento":False}
serial_coxxxxds['EnableUserEntry'] = {"serial":"xxxx","complemento":False}
serial_coxxxxds['Reboot'] = {"serial":"xxxx","complemento":False}


#################
### Args control
#################

def get_arg(arg):
    """
    get arg content 
    """
    global opts
    output = None
    for o in opts:
        if type(o) != tuple:
            o = [o]

        if o[0] in arg:
            output = o[1]

    return output

try:
    argv = sys.argv
    opts, argv = getopt.getopt(argv[1:], "sa:i:c:q:", ["start","auto=","ip=",'commandline=','queue='])
    opts += argv

except getopt.GetoptError, err:
	print >>sys.stderr, err.msg
	print >>sys.stderr, "for help use --help"
	sys.exit(1)