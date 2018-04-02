#------------------------------------------------------------------------------#
# interactive_frame.py                                                         #
#                                                                              #
#------------------------------------------------------------------------------#

# PYTHON MODULES
import Tkinter as tk
import logging, threading, time, sys

#------------------------------------------------------------------------------#
#                         STREAM REDIRECTORS                                   #
#                                                                              #
# The redirectors InRedirector and OutRedirector take the stdin and stdout     #
# streams and overwrite their usual functionality so that the streams interact #
# with the custom-made terminal emulator.                                      #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# InRedirector                                                                 #
#                                                                              #
# This class is used in OutRedirector to handle the stdin stream.              #
#                                                                              #
# WARNING: There should only be one instance of this class                     #
#------------------------------------------------------------------------------#

class InRedirector:
    def __init__(self, outRedirector):
        self.outRedirector = outRedirector

    def readline(self):
        line = ""
        # Keep checking whether a line has been entered into the 'terminal'
        while not line:
            line = self.outRedirector.getInputLine()
            time.sleep(0.1)
        return line

#------------------------------------------------------------------------------#
# OutRedirector                                                                #
#                                                                              #
# This is a Tkinter Text widget that overwrites the stdout stream to output    #
# all stdout to the widget.                                                    #
#                                                                              #
# WARNING: There should only be one instance of this class                     #
#------------------------------------------------------------------------------#
class OutRedirector(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # Save old stdout
        self.old_stdout = sys.stdout

        self.edit_begin = "1.0"

        # Redirect all standard output through this object
        sys.stdout = self
        
        self.input_buffer = ""
        self.input_lines = []

        key_bindings = {
            "<Key>"       : self.key,
            # To be implemented
            # "<BackSpace>" : self.key_backspace,
            # "<Prior>"     : self.key_prior,
            # "<Next>"      : self.key_next,
            # "<End>"       : self.key_end,
            # "<Home>"      : self.key_home,
            # "<Left>"      : self.key_left,
            # "<Up>"        : self.key_up,
            # "<Right>"     : self.key_right,
            # "<Down>"      : self.key_down,
            # "<Delete>"    : self.key_delete,
            }

        # Control use of different keys based on dictionary
        for key in key_bindings:
            self.bind(key, key_bindings[key])
        
        # Save old stdin
        self.old_stdin = sys.stdin

        # Redirect all stdin queries to the InRedirector
        sys.stdin = InRedirector(self)

    def key(self, key):
        if key.char():
            # Store the new character in the buffer
            self.input_buffer += key.char
            if key.char == '\r' or key.char == '\n':
                # When the user presses the enter key, 
                # add the buffer to input_lines and clear the buffer
                self.input_lines.append(self.input_buffer[:-1] + '\n')
                self.input_buffer = ""

    def getInputLine(self):
        '''
        Returns the next line from input_lines (used as a queue)
        If input_lines is empty return None
        '''

        if self.input_lines == []:
            return None
        line = self.input_lines[0]
        self.input_lines = self.input_lines[1:]
        return line

    def write(self, s):
        # This is called by print and sys.stdout.write(...)
        self.insert("end", s)
        self.update()

        # Update edit_begin pointer
        self.edit_begin = self.index("insert")

#------------------------------------------------------------------------------#
# ErrorHandler                                                                 #
#                                                                              #
#------------------------------------------------------------------------------#

class ErrorHandler(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.config(state="disabled")

    def write(self, s):
        self.config(state="normal")
        self.insert("end", s)
        self.config(state="disabled")
        self.update()

    def flush(self):
        pass

#------------------------------------------------------------------------------#
# InteractiveFrame                                                             #
#------------------------------------------------------------------------------#

class InteractiveFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
        terminal = OutRedirector(self)
        terminal.grid(row=0, column=0, sticky="nsew")
        
        err = ErrorHandler(self)
        err.grid(row=1, column=0, sticky="nsew")

        # Setup logging control for error handler
        logger = logging.getLogger("cspy.error_log")
        logger.setLevel(loggingLevel)

        handler = logging.StreamHandler(err)
        handler.setLevel(loggingLevel)

        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        self.thread = None

        sys.path.append(cspy_master_path)

    def runCSPyProgram(self, cspy_file_name):
        '''
        If the class's thread is currently unused this program runs the
        cspy_master.py program with cspy_file_name as its argument.
        '''
        if self.thread == None or \
                not self.thread.isAlive():
            
            # Previous program is done so a new one can be started
            sys.argv = [cspy_master_path + "cspy_master.py",
                        cspy_file_name]

            import cspy_master

            self.thread = threading.Thread(target=cspy_master.main)
            self.thread.deamon = True  # end thread if main program ends
            self.thread.start()        # run the program

        else:
            # Program still running - a new program should not be started
            logger = logging.getLogger("cspy.error_log")
            logger.warning("Program cannot be started while another" +
                           " program is running")

loggingLevel = logging.WARNING
cspy_master_path = "/home/acampbel/CSPy-shared/ulysses/magnus_programs/cspy_code"