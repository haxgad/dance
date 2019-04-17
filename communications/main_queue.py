import threading
import logging
from csv import writer
from queue import Queue
import sys
import logging
import os.path
from collections import deque, Counter

from UART_client import UARTClient
from classifier import Classifier
from eval_server.socket_client import SocketClient


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
BUF_SIZE = 50
q = Queue()
# clf = Classifier('/home/pi/comms/window50_model.h5')
#clf = Classifier('/home/pi/dance/communications/test_model.sav')
clf = Classifier('/home/pi/dance/communications/window50_model.sav')
# print(clf.predict(dataset[157:182]))


class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread,self).__init__()
        print("Producer ready")
        self.target = target
        self.name = name

        # Initialize connection to Arduino
        self.client = UARTClient('/dev/ttyAMA0')
        # self.client.handshake()

    def run(self):
        buffer = []
        index = 0

        # Get filename to output data
        count = 0
        prefix_name = '/home/pi/comms/output'
        while os.path.isfile(prefix_name + str(count) + '.txt'):
            count += 1
        filename = prefix_name + str(count) + '.txt'

        while 1:
            try:
                data_list, error = self.client.receive_serialized_data()
                # ToDo: Log power later

                with open(filename, 'a') as csv_file:
                    writer_obj = writer(csv_file)
                    data_list, error = self.client.receive_serialized_data()
                    print("Index: {}".format(index))
                    logger.info("Index:p {}".format(index))
                    index += 1
                    writer_obj.writerow(data_list)

                if data_list:
                    buffer.append((data_list[:15], data_list[15:]))
                    logger.info("Index: {}".format(index))
                    index += 1
                else:
                    logger.error("Comms - {}".format(str(error)))

                # Send the 20-row package to ML model
                if len(buffer) >= BUF_SIZE:
                    q.put(buffer)

                    # Clear the buffer for new data
                    #buffer = buffer[BUF_SIZE/2:]
                    buffer = []
                    
            except Exception as exc:
                #logger.error("Comms - {}".format(str(exc)))
                print(str(exc))


class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread,self).__init__()
        print("Consumer ready")
        self.target = target
        self.name = name
        self.logger = create_logger('ML', '/home/pi/comms/ml_output.log')
        
        # Connect to eval server
#        ip_addr = "192.168.43.180"
#        #ip_addr = "192.168.43.51"
#        port = 8889
#        self.socket_client = SocketClient(ip_addr, port)
#        while 1:
#            try:
#                self.socket_client.connect()
#                break
#            except Exception as exc:
#                print(str(exc))
#        
#        print('Server connected')
                

    def run(self):
        queue = deque()
        count = 0
        prev = -1
        action_mapping = {
             0: 'chicken',
             1: 'cowboy',
             2: 'cowboy',
             3: 'crab',
             4: 'hunchback',
             5: 'raffles',
             6: 'raffles',
             7: 'runningman',
             8: 'jamesbond',
             9: 'snake',
             10:'doublepump',
             11:'mermaid',
             12:'final'
        }
        while 1:
            if not q.empty():
                item = q.get()
                data_list = [ele[0] for ele in item]
                _, voltage, current, cumpower = item[-1][1]
                
                # Insert code to call the ML here
                # ...
                predicted_move = clf.predict(data_list)[0]

                # Send the result
                # As the WiFi is not working, log the output to file
                self.logger.info(predicted_move)
                print(action_mapping[predicted_move])
                
                if predicted_move != prev:
                    prev = predicted_move
                    count = 1
                    continue
                count += 1
                
#                if count >= 3:
#                    self.logger.info("PREDICT: {}".format(predicted_move))
#                    self.socket_client.send_data(
#                        action_mapping[int(predicted_move)],
#                        voltage / 1000,
#                        current / 1000,
#                        voltage*current / 1000000,
#                        cumpower
#                    )
#                    count = 0
                        
            #try:
                        
            #except Exception as exc:
            #    logger.error("ML - {}".format(str(exc)))


if __name__ == '__main__':
    p = ProducerThread(name='producer')
    c = ConsumerThread(name='consumer')

    p.start()
    c.start()
