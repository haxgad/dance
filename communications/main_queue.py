import threading
import logging
from queue import Queue
import sys
import logging

from classifier import Classifier

def create_logger(name, filename='/home/pi/comms/comms.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create a file handler
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    return logger

# Initialise
logger = create_logger('root')
BUF_SIZE = 25
q = Queue()
clf = Classifier('/home/pi/comms/dance_data_Mar_26_model.h5')
# print(clf.predict(dataset[157:182]))


class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread,self).__init__()
        self.target = target
        self.name = name

        # Initialize connection to Arduino
        self.client = UARTClient('/dev/ttyAMA0')
        self.client.handshake()

    def run(self):
        buffer = []
        index = 0
        while 1:
            try:
                data_list, error = self.client.receive_serialized_data()
                if data_list:
                    buffer.append(data_list[:15])
                    logger.info("Index: {}".format(index))
                    index += 1
                else:
                    logger.error("Comms - {}".format(str(error)))

                # Send the 20-row package to ML model
                if len(buffer) >= BUF_SIZE:
                    q.put(buffer)

                    # Clear the buffer for new data
                    buffer = []
            except Exception as exc:
                logger.error("Comms - {}".format(str(exc)))


class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread,self).__init__()
        self.target = target
        self.name = name
        self.logger = create_logger('ML', '/home/pi/comms/ml_output.log')

    def run(self):
        while 1:
            try:
                if not q.empty():
                    item = q.get()

                    # Insert code to call the ML here
                    # ...
                    predicted_move = clf.predict(item)[0]

                    # Send the result
                    # As the WiFi is not working, log the output to file
                    self.logger.info(predicted_move)
            except Exception as exc:
                logger.error("ML - {}".format(str(exc)))


if __name__ == '__main__':
    p = ProducerThread(name='producer')
    c = ConsumerThread(name='consumer')

    p.start()
    c.start()
