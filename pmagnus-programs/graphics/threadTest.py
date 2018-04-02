import threading
import os, time, select, sys

def std_reader():
    while True:
        if sys.stdout.

std_thread = threading.Thread(target=std_reader)

std_thread.setDaemon(True)
std_thread.start()
for i in range(10):
    sys.stdout.write("hi")
    sys.stdout.flush()
    time.sleep(5)