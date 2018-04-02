import logging
import time

def fun(arg):
    logger = logging.getLogger("error_logger")
    if logger.handlers == []:
        logging.basicConfig(level=logging.ERROR,
                            format='%(message)s')
    while not arg['stop']:
        print 'hello'
        name = raw_input("What is your name? ")
        logger.error("Hi " + name + "!")
        time.sleep(0.5)

if __name__ == "__main__":
    fun({'stop' : False})