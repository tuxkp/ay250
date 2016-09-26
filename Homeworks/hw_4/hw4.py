#%%time
import logging
import random
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

import threading

def worker(num):
    """thread worker function"""
    
    sleep_time = random.randint(1,5)
    logging.debug('worker: {0} sleeping for {1} s, name: {2}'
                   .format(num,sleep_time,threading.current_thread().getName()))
    time.sleep(sleep_time)
    logging.debug('done')
    return

#threads = []
#for i in range(10):
#    t = threading.Thread(target=worker, args=(i,))
#    threads.append(t)
#    t.start()
##    t.join()


#threads = []
#for i in range(10):
#    t = threading.Thread(target=worker, args=(i,))
#    threads.append(t)

#print("waiting around a bit, then starting threads",flush=True)
#time.sleep(2)

# dont have to start a thread immediately after creating them
#for t in threads:
#    t.start() 

#for t in threads:
#    t.start()
#    t.join() # this waits for the thread to finish



#threads = []
#for i in range(2):
#    r = random.randint(1,5)
#    t = threading.Timer(r, worker, args=(i,))
#    threads.append(t)
#    logging.debug("starting {0} with delay {1}"
#                  .format(t.getName(),r))
#    threads[-1].start()

from queue import Queue

q = Queue()

def worker2(num):
    sleep_time = random.randint(1,5)
    
    logging.debug('worker: {0} sleeping for {1} s, name: {2}'
                   .format(num,sleep_time,threading.current_thread().getName()))
    time.sleep(sleep_time)

    if q.empty():
        q.put(sleep_time)
        logging.debug("initiated q = {0}".format(sleep_time))
    else:
        var = q.get()
        logging.debug("var {0}".format(var))
        q.put(sleep_time + var)
        logging.debug("added {0} to the q".format(sleep_time))
        
    logging.debug('done')
    return

threads = []
for i in range(2):
    t = threading.Thread(target=worker2, args=(i,))
    threads.append(t)
    t.start()

