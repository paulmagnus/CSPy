#------------------------------------------------------------------------------#
# cspy_runtime.py                                                              #
#                                                                              #
# Written by Maya Montgomery '18                                               #
# June 2016                                                                    #
#                                                                              #
# Revised and edited by Paul Magnus '18, Ines Ayara and Matthew R. Jenkins '20 #
# Summer 2017                                                                  #
#                                                                              #
# A runtime handler, the final step in the execution of the language CSPy, a   #
# dialect of Python. Runs the Python executable, catches and reports any run-  #
# time errors (substituting CSPy file line numbers for the Python executable   #
# line numbers), and deletes the Python and line map files when finished.      #
#                                                                              #
# USAGE: (ENTER THESE LINES INTO MASTER PROGRAM)                               #
#        from cspy_runtime import *                                            #
#                ...                                                           #
#        run(filename.cspy)                                                    #
#------------------------------------------------------------------------------#

# PYTHON IMPORTS
import getpass, sys, re, logging

tmp_path = "/tmp" + getpass.getuser()

class ExceptionHandler:
    def __init__(self, imports, path, overloads):
        self.imports = imports
        self.path = path
        self.overloads = overloads

        # save the old stderr
        self.old_stderr = sys.stderr
        # overwrite so that all error messages are sent to this class
        sys.stderr = self

        # add logging support
        logging.basicConfig(level=logging.ERROR, format='%(message)s')
        self.logger = logging.getLogger("cspy.error_log")

    def write(self, s):
        err = s.split("\n")
        if len(err) == 1:
            self.old_stderr.write(s)
        err = err[:len(err)-1]  # get rid of ending \n
        error_msg = err[len(err) - 1]

        # check for overloaded name in error message
        for env in overloads:
            for key in overloads[env]:
                if key in error_msg:
                    # overloaded name found
                    # replace all instances of overloaded name with cspy name
                    error_msg = error_msg.replace(key, overloads[env][key])
                    
        trace_lines = []
        
        # COLLECT TRACEBACK FOR CSPY FILES
        trace = []
        for i in range(len(err)):
            if "Traceback" in err[i]:
                trace_lines = err[i+1:len(err) - 1] # list of traceback lines
                break

        for x in range(0, len(trace_lines), 2):
            line = trace_lines[x]            # 0: file info
            bad_code = trace_lines[x+1]      # 1: line of code
            line_info = []                   # to save info from loop

            # GET FILE NAME AND LINE NUMBER
            REX = re.compile('File \"(?P<f>[\S]+)\.py\", line (?P<n>[0-9]+)')
            found = REX.search(line)

            if found:
            
                line_num = int(found.group("n"))  # Python line number
                f_name = found.group("f")         # file name pos. w/ path
            
                # handle path if applicable
                find_path = re.compile('(?P<p>[\S]+/)(?P<f>[\S]+)')
                found_path = find_path.search(f_name)
                if found_path:
                    f_name = found_path.group("f")   # file name, no path

                if f_name + ".cspy" in imports:
                    map_name = tmp_path + "/" + f_name + "_linemap"
                    
                    # IMPORT LINE MAP
                
                    try:
                        line_map = pickle.load(open(map_name, "rb"))
                    except IOError:
                        self.logger.critical("\nError: file '" + f_name + 
                                          ".cspy not correctly compiled: " +
                                          "line map does not exist.")
                        # print >> self.old_stderr, "\nError: file '" + f_name + \
                        #     ".cspy' not correctly compiled: " + \
                        #     "line map does not exist."
                        remove_files()              # clean up & terminate

                    # SAVE LINE INFO
                    try:
                        line_num = line_map[line_num]  # convert to CSPy value
                    except KeyError:
                        self.logger.critical("\nError: file '" + f_name +
                                          ".cspy' not correctly compiled:\n" +
                                          "line map file does not accurately map " +
                                          ".cspy to Python.")
                        # print >> self.old_stderr, "\nError: file '" + f_name + \
                        #     ".cspy' not correctly compiled;\n" + \
                        #     "line map file does not accurately map " +\
                        #     ".cspy to Python."
                        remove_files()                 # clean up & terminate

                    line_info.append(path + f_name + ".cspy")
                    line_info.append(line_num)

                    # bad_code is from PY file, not CSPy file
                    # save file name, CSPy file line number, and line of code
                    trace.append([line_info[0], line_info[1], bad_code])

                else:
                    # error in python file nor CSPy file
                    if found_path:
                        trace.append([found_path.group("p") + f_name + ".py",
                                      line_num, bad_code])
                    else:
                        trace.append([f_name + ".py",
                                      line_num, bad_code])

        # REPORT ERROR
        if (trace == []):              # error in CSPy system, not a .cspy file
            self.logger.critical("\nError: issue with CSPy environment files.")
            # print >> self.old_stderr, "\nError: issue with CSPy environment files."
            for l in err:
                self.logger.error(l)
                # print >> self.old_stderr, l
            remove_files()                             # clean up & terminate

        line = trace[len(trace)-1]                     # get actual error

        self.logger.error("\nTHERE IS AN ERROR IN FILE '" + line[0] +
                          "', LINE " + str(line[1]) + ":")
        # print >> self.old_stderr, "\nTHERE IS AN ERROR IN FILE '" + \
        #     line[0] + "', LINE " + \
        #     str(line[1]) + ":"

        # the actual bad code from CSPy file    
        self.logger.error(linecache.getline(line[0], line[1]))
        # print >> self.old_stderr, linecache.getline(line[0], line[1])

        self.logger.error("\n" + error_msg)
        # print >> self.old_stderr, "\n" + error_msg                   # and the error msg

        # PRINT TRACEBACK
        if (len(trace) > 1):
            self.logger.error("\n\nTRACEBACK:")
            # print >> self.old_stderr, "\n\nTRACEBACK:"
            for line in trace:
                self.logger.error("File '" + line[0] + "', line " +
                                  str(line[1]) + ":")
                # print >> self.old_stderr, "File '" + line[0] + "', line " \
                #     + str(line[1]) + ":"
                
                self.logger.error(linecache.getline(line[0], line[1]))
                # print >> self.old_stderr, linecache.getline(line[0], line[1])
    
        remove_files()                                     # clean up & terminate


def run(filename, pyimports, path, overloads):

    logging.basicConfig(level=logging.ERROR, format='%(message)s')
    logger = logging.getLogger("cspy.error_log")
    
    # LOCATE PYTHON EXECUTABLE
    find_path = re.compile('(?P<p>[\S]+)/(?P<n>[\S]+).cspy')
    found_path = find_path.search(filename)

    if found_path:
        name_no_ext = found_path.group("n")
    else:
        name_no_ext = filename[:len(filename)-5]

    name_py = name_no_ext + ".py"

    # CONFIRM FILE EXISTS
    if not os.path.isfile(tmp_path + "/" + name_py):
        logger.critical("\nError: file '" + tmp_path + "/" + 
                     name_no_ext + ".cspy' not correctly compiled:\n" +
                     "Python executable file does not exist.")
        # print >> sys.stderr, "\nError: file '" + tmp_path + "/" + \
        #     name_no_ext +  ".cspy' not correctly compiled:\n" + \
        #     "Python executable file does not exist."
        remove_files()

    # Build caller file
    f = open(tmp_path + "/_cspy_caller.py", "w")
    f.write("from " + name_no_ext + " import _cspy_main\n" +
                "def _cspy_caller():\n\t_cspy_main()")
    f.close()

    # RUN PYTHON PROGRAM
    # Run all error outputs through the exception handler
    handler = ExceptionHandler(pyimports, path, overloads)
    sys.path.append(tmp_path)

    # This import done to ensure that no variables will be affected in this file
    try:
        import _cspy_caller
    except:
        logger.critical("\nError: Runtime python execute error in" +
                        " 'cspy_runtime.py'")
        # print >> sys.stderr, "Error: Runtime python execute error in" +\
        #     " 'cspy_runtime.py'"

    _cspy_caller._cspy_caller()

    sys.stderr = handler.old_stderr

    remove_files()

def remove_files():
    # Remove the temporary folder
    shutil.rmtree(tmp_path)
    sys.exit(0)