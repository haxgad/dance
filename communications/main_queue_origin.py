import threading
import time
import logging
import random
from queue import Queue
import sys

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

BUF_SIZE = 10
q = Queue()

class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread,self).__init__()
        self.target = target
        self.name = name

    def run(self):
        while 1:
            try:
                if not q.full():
                    item = random.randint(1,10)
                    q.put(item)
                    logging.debug('Putting ' + str(item)
                                  + ' : ' + str(q.qsize()) + ' items in queue')
                    time.sleep(1)
            except KeyboardInterrupt:
                sys.exit()


class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread,self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        while 1:
            try:
                if not q.empty():
                    item = q.get()
                    logging.debug('Getting ' + str(item)
                                  + ' : ' + str(q.qsize()) + ' items in queue')
                    # time.sleep(random.random())
            except KeyboardInterrupt:
                sys.exit()

if __name__ == '__main__':

    p = ProducerThread(name='producer')
    c = ConsumerThread(name='consumer')

    p.start()
    c.start()
