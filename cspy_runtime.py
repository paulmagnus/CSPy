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
import sys, re, os, subprocess, importlib, getpass, shutil, pickle, linecache

tmp_path = "/tmp/" + getpass.getuser()

def run(filename, imports, path, overloads):
    
    # LOCATE PYTHON EXECUTABLE
    find_path = re.compile('(?P<p>[\S]+)/(?P<n>[\S]+).cspy')
    found_path = find_path.search(filename)
    
    if found_path:
        name_no_ext = tmp_path + "/" + found_path.group("n")
    else:
        name_no_ext = tmp_path + "/" + filename[:len(filename)-5]

    name_py = name_no_ext + ".py"

    # CONFIRM FILE EXISTS
    if not os.path.isfile(name_py):
        print >> sys.stderr, "\nError: file '" + name_no_ext + \
              ".cspy' not correctly compiled;\n" + \
              "Python executable file does not exist."
        remove_files()                                 # clean up & terminate

    # ATTEMPT TO RUN EXECUTABLE

    # pipe errors into file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    if found_path:
        os.system(script_dir + '/bin/.run_python.sh ' + name_py +
                  ' ' + found_path.group("p") + ' 2> ' +  tmp_path + '/err.txt')
    else:
        os.system(script_dir + '/bin/.run_python.sh ' + name_py +
                  ' ./ 2> ' + tmp_path + '/err.txt')

    err = open(tmp_path + '/err.txt').read()

    # HANDLE EXCEPTION
    if (err != ""):
        handle_exception(err, imports, path, overloads)
    
    remove_files()                                     # clean up & terminate

#------------------------------------------------------------------------------#
#                            EXCEPTION HANDLER                                 #
#------------------------------------------------------------------------------#

def handle_exception(err, imports, path, overloads):

    err = err.split("\n")
    err = err[:len(err)-1]            # get rid of ending \n
    error_msg = err[len(err) - 1]

    # check for overloaded name in the error message
    #
    # NOTE: IF ERROR OUTPUT SEEMS TO HAVE VERY STRANGE WORDS IN IT, THIS IS
    # PROBABLY THE SOURCE OF THE ERROR
    for env in overloads:
        for key in overloads[env]:
            if key in error_msg:
                # overloaded name found
                # replace all instances of overloaded name with cspy name
                error_msg = error_msg.replace(key, overloads[env][key])

    # print "err", err           # debug

    trace_lines = []

    # COLLECT TRACEBACK FOR CSPY FILES
    trace = []
    for i in range(len(err)):
        if "Traceback" in err[i]:
            trace_lines = err[i+1:len(err) - 1]     # list of traceback lines
            break

    import_names = []

    for s in imports:
        # print s
        find_path = re.compile('(?P<p>[\S]+)/(?P<n>[\S]+\.cspy)')
        found_path = find_path.search(s)
        if found_path:
            import_names.append(found_path.group('n'))

    if import_names == []:
        import_names = imports

    if len(trace_lines) % 2 != 0:
        # remove trailing odd line
        trace_lines = trace_lines[:-1]

    for x in range(0, len(trace_lines), 2):
            
        line = trace_lines[x]            # 0: file info
        bad_code = trace_lines[x+1]      # 1: line of code
        line_info = []                   # to save info from loop
        
        # GET FILE NAME AND LINE NUMBER
        REX = re.compile('File \"(?P<f>[\S]+)\.py\", line (?P<n>[0-9]+)')
        found = REX.search(line)

        if not found:
            REX = re.compile("File \'(?P<f>[\S]+)\.py\', line (?P<n>[0-9]+)")
            found = REX.search(line)

        if found:
            
            line_num = int(found.group("n"))  # Python line number
            f_name = found.group("f")         # file name pos. w/ path
            
            # handle path if applicable
            find_path = re.compile('(?P<p>[\S]+/)(?P<f>[\S]+)')
            found_path = find_path.search(f_name)

            if found_path:
                f_name = found_path.group("f")   # file name, no path

            if f_name + ".cspy" in import_names:
                map_name = tmp_path + "/" + f_name + "_linemap"
                    
                # IMPORT LINE MAP
                
                try:
                    line_map = pickle.load(open(map_name, "rb"))
                except IOError:
                    print >> sys.stderr, "\nError: file '" + f_name + \
                          ".cspy' not correctly compiled: " + \
                          "line map does not exist."
                    remove_files()              # clean up & terminate
                    exit()

                # SAVE LINE INFO
                try:
                    line_num = line_map[line_num]  # convert to CSPy value
                except KeyError:
                    print >> sys.stderr, "\nError: file '" + f_name + \
                          ".cspy' not correctly compiled;\n" + \
                          "line map file does not accurately map " +\
                          ".cspy to Python."
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
        print >> sys.stderr, "\nError: issue with CSPy environment files."
        for l in err:
            print >> sys.stderr, l
        remove_files()                             # clean up & terminate
        exit()

    
    line = trace[len(trace)-1]                     # get actual error

    print >> sys.stderr, "\nTHERE IS AN ERROR IN FILE '" + \
          line[0] + "', LINE " + \
          str(line[1]) + ":"

    # the actual bad code from CSPy file
    print >> sys.stderr, linecache.getline(line[0], line[1])
    
    print >> sys.stderr, "\n"
    print >> sys.stderr, error_msg

    # PRINT TRACEBACK
    if (len(trace) > 1):
        print >> sys.stderr, "\n\nTRACEBACK:"
        for line in trace:
            print >> sys.stderr, "File '" + line[0] + "', line " \
                  + str(line[1]) + ":"
                
            print >> sys.stderr, linecache.getline(line[0], line[1])
    
    remove_files()                                     # clean up & terminate

# REMOVE ALL TRACES OF COMPILATION
def remove_files():
    try:                                             # it should exist, but jic
        shutil.rmtree(tmp_path)
    finally:
        sys.exit(0)