from app.auto import Auto
from cfg import *

class AutoCommandLine(Auto):

    def __init__(self, interface):
        Auto.__init__(self, interface)


    def wait_exec(self):
        """
        Really wait for the time defined or by a click on the box
        """
        sec_time = self.sec_time
        self.show_message("Waiting ddd " + str(sec_time) + " seconds")
        time.sleep(sec_time)
        self.step()



    def step(self):
        """
        Execute the script line by line
        """
        if not self.play_cmd:
            return False

        line = self.get()
        self.warn_observers('step')
        if(line):
            if line[0] != '#':
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
            self.warn_observers('stop')