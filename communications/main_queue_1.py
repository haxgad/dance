from multiprocessing import Process, Queue, Lock
import logging
from csv import writer
import sys
import os.path

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
# logger = create_logger('root')
# BUF_SIZE = 50
# clf = Classifier('/home/pi/comms/window50_model.h5')
#clf = Classifier('/home/pi/dance/communications/test_model.sav')
clf = Classifier('/home/pi/dance/communications/window50_model.sav')

# Producer function that places data on the Queue
def producer(queue, lock):
    # Init producer
    logger = create_logger('root')
    BUF_SIZE = 50
    client = UARTClient('/dev/ttyAMA0')
    buffer = []
    index = 0
    print('Producer ready')

    # Get filename to output data
    # count = 0
    # prefix_name = '/home/pi/comms/output'
    # while os.path.isfile(prefix_name + str(count) + '.txt'):
    #     count += 1
    # filename = prefix_name + str(count) + '.txt'

    while 1:
        data_list, error = client.receive_serialized_data()
        if error:
            logger.error(str(error))
            continue

        if data_list:
            buffer.append((data_list[:15], data_list[15:]))
            logger.info("Index: {}".format(index))
            index += 1

        # Send the 20-row package to ML model
        if len(buffer) >= BUF_SIZE:
            with lock:
                q.put(buffer)
                buffer = []


# The consumer function takes data off of the Queue
def consumer(queue, lock):
    # Init consumer
    clf = Classifier('/home/pi/dance/communications/window50_model.sav')
    logger = create_logger('ML', '/home/pi/comms/ml_output.log')
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
    print('Consumer ready')

    while 1:
        # If the queue is empty, queue.get() will block until the queue has data
        item = queue.get()
        data_list = [ele[0] for ele in item]
        _, voltage, current, cumpower = item[-1][1]

        # Insert code to call the ML here
        # ...
        predicted_move = clf.predict(data_list)[0]
        logger.info(predicted_move)

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

if __name__ == '__main__':
    # Create the Queue object
    queue = Queue()

    # Create a lock object to synchronize resource access
    lock = Lock()

    producer = Process(target=producer, args=(queue, lock))
    consumer = Process(target=consumer, args=(queue, lock))

    producer.start()
    consumer.start()

    # Try running without join
    # And enable `join` for producer only
    # producer.join()
    # consumer.join()
