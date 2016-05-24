from cfg import *

from Remote import Remote
from app.AutoCommandLine import AutoCommandLine
import datetime

class AutomateCommandLine(object):
    """description of class"""

    def __init__(self, ip, queue, script_file):
        self.log = {}
        self.ip = []
        if queue is not None:
            self.ip = self.get_ip(queue)
        else:
            self.ip.append(ip)

        self.create_log(script_file)

        self.auto = AutoCommandLine(self)

        self.auto.load_script(script_file)
        self.auto.run_script()

    def create_log(self, script_file):
        pos = script_file.find('.shef')
        path = 'log/' + script_file[0:pos] + '/'
        if not os.path.exists(path):
            os.mkdir(path)
        
        for ip in self.ip:
            log = open(path + ip + '.txt', 'w')
            self.log[ip] = log


    def get_ip(self, filename):
        file = open(filename)
        ips = []
        for ip in file.readlines():
            ips.append(ip.strip())
        file.close()
        return ips

    def show_message(self, msg, tag="default"):
        pass
        #print msg


    def make_rem_readable(self, msg, tag="default"):
        message = "hold: " + msg['hold']+"\n"
        message += "key: " + msg['key'] +"\n"
        message += "status: \n"
        message += "\tcode: " + str(msg['status']['code']) +"\n"
        message += "\tCommand Result: " + str(msg['status']['commandResult']) +"\n"
        message += "\tmsg: " + str(msg['status']['msg']) +"\n"
        message += "\tquery: " + str(msg['status']['query']) +"\n"
        message += "------------------------------------------------------\n\n"

        return message

    def send(self, key, hold):
        resp = True
        for ip in self.ip:
            rem = Remote(ip)
            print 'processing: ip: %s, key: %s, hold: %s, date: %s'%(ip, key, hold, datetime.datetime.today())           
            
            ret = rem.send(hold, key)
            #self.log[ip].write("ip: %s\n"%(ip))

            if ret is not None:
                if rem.return_is_valid(ret, key, hold):
                    print 'processed'
                    self.log[ip].write(self.make_rem_readable(ret))
                else:          
                    print 'failed'
                    self.ip.remove(ip)
                    self.log[ip].write(self.make_rem_readable(ret))
                    self.log[ip].close()
            else:
                self.ip.remove(ip)
                print 'Timeout Connection'
                message = "Timeout Connection\n"
                message += "------------------------------------------------------\n\n"
                self.log[ip].write(message)
                self.log[ip].close()

        return True if len(self.ip) else False


    def close_files(self):
        for ip in self.ip:
            self.log[ip].close()


