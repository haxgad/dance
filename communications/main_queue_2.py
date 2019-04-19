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
# clf = Classifier('/home/pi/comms/dance_data_Mar_26_model.h5')
# clf = Classifier('/home/pi/dance/communications/test_model.sav')
# print(clf.predict(dataset[157:182]))


class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread,self).__init__()
        self.target = target
        self.name = name

        # Initialize connection to Arduino
        self.client = UARTClient('/dev/ttyAMA0')
        # self.client.handshake()

    def run(self):
        global q
        buffer = []
        index = 0

        # Get filename to output data
        count = 0
        #prefix_name = '/home/pi/comms/output'
        #while os.path.isfile(prefix_name + str(count) + '.txt'):
        #    count += 1
        #filename = prefix_name + str(count) + '.txt'
        print("Producer ready")
        
        while 1:
            data_list, error = self.client.receive_serialized_data()
            if error:
                logger.error("Comms - {}".format(str(error)))
                continue
            
            # try:
            #     with open(filename, 'a') as csv_file:
            #         writer_obj = writer(csv_file)
            #         data_list, error = self.client.receive_serialized_data()
            #         # print("Index: {}".format(index))
            #         logger.info("Index: {}".format(index))
            #         index += 1
            #         writer_obj.writerow(data_list)
            # except Exception as exc:
            #     logger.debug(str(exc))

            if data_list:
                buffer.append((data_list[:15], data_list[15:]))
                logger.info("Index: {}".format(index))
                #print("Index: {}".format(index))
                #print(data_list)
                index += 1

            # Send the 20-row package to ML model
            if len(buffer) >= BUF_SIZE:
                q.put(buffer)
                # Clear the buffer for new data
                buffer = buffer[25:]
                #buffer = []

class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread,self).__init__()
        
        self.target = target
        self.name = name
        self.logger = create_logger('ML', '/home/pi/comms/ml_output.log')
        #self.clf = Classifier('/home/pi/dance/communications/window50_model.sav')
        #self.clf = Classifier('/home/pi/dance/software/final_models/window50_model.h5')
        self.clf = Classifier(
            '/home/pi/dance/software/final_models/model_1.joblib',
            '/home/pi/dance/software/final_models/scaler_1.joblib'
        )
        # Connect to eval server
        ip_addr = "192.168.43.51"

        # Prof's IP
        #ip_addr = "192.168.43.51"
        
        # Using my hotspot
        #ip_addr = "172.20.10.10"

        port = 8888
        print('Prepare to connect to server')
        self.socket_client = SocketClient(ip_addr, port)
        while 1:
            try:
                self.socket_client.connect()
                break
            except Exception as exc:
                print(str(exc))
        print('Server connected')


    def run(self):
        global q
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
        print("Consumer ready")
        
        while 1:
            item = q.get()
            q.task_done()    
            #print('Prepare to predict')
        
            data_list = [ele[0] for ele in item]
            _, voltage, current, cumpower = item[-1][1]
            #print(data_list)
            
            # Insert code to call the ML here
            # ...
            predicted_move = self.clf.predict(data_list)[0]
            #try:
            #    predicted_move = self.clf.predict(data_list)[0]
            #except Exception as exc:
            #    self.logger.error(str(exc))
                
            # Send the result
            self.logger.info(action_mapping[int(predicted_move)])
            #print(action_mapping[int(predicted_move)])
            
            if predicted_move != prev:
                prev = predicted_move
                count = 1
                continue
            count += 1
            
            # Send all predictions
#            self.socket_client.send_data(
#                    action_mapping[int(predicted_move)],
#                    voltage / 1000,
#                    current / 1000,
#                    voltage*current / 1000000,
#                    cumpower
#            )
            
            if count >= 3:
                self.logger.info("PREDICT: {}".format(predicted_move))
                self.socket_client.send_data(
                    action_mapping[int(predicted_move)],
                    voltage / 1000,
                    current / 1000,
                    voltage*current / 1000000,
                    cumpower
                )
                count = 0



if __name__ == '__main__':
    p = ProducerThread(name='producer')
    c = ConsumerThread(name='consumer')

    p.start()
    c.start()
