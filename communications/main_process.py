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
import multiprocessing as mp


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
BUF_SIZE = 10
q = Queue()
# clf = Classifier('/home/pi/comms/dance_data_Mar_26_model.h5')
clf = Classifier('/home/pi/dance/communications/test_model.sav')
# print(clf.predict(dataset[157:182]))

def producer(queue):
    # Init
    client = UARTClient('/dev/ttyAMA0')
    buffer = []
    index = 0

    # Get filename to output data
    count = 0
    prefix_name = '/home/pi/comms/output'
    while os.path.isfile(prefix_name + str(count) + '.txt'):
        count += 1
    filename = prefix_name + str(count) + '.txt'

    print("Producer ready")
    while 1:
        try:
            data_list, error = client.receive_serialized_data()
            # ToDo: Log power later

            with open(filename, 'a') as csv_file:
                writer_obj = writer(csv_file)
                data_list, error = client.receive_serialized_data()
                # print("Index: {}".format(index))
                logger.info("Index: {}".format(index))
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
                buffer = []
        except Exception as exc:
            logger.error("Comms - {}".format(str(exc)))


def consumer(queue):
    # Init
    ml_logger = create_logger('ML', '/home/pi/comms/ml_output.log')
    queue = deque()
    count = 0
    prev = -1
    action_mapping = {
         0: 'chicken',
         1: 'cowboy',
         2: 'crab',
         3: 'hunchback',
         4: 'raffles'
    }
    print("Consumer ready")

    ip_addr = "192.168.43.180"
    port = 8889
    socket_client = SocketClient(ip_addr, port)

    # Connect to server before starting sending data
    while 1:
        try:
            socket_client.connect()
            break
        except Exception as exc:
            print(str(exc))

    print('Server connected')

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
            ml_logger.info(predicted_move)

            if predicted_move != prev:
                prev = predicted_move
                count = 1
                continue
            count += 1

            if count >= 3:
                ml_logger.info("PREDICT: {}".format(predicted_move))
                socket_client.send_data(
                    action_mapping[int(predicted_move)],
                    voltage / 1000,
                    current / 1000,
                    voltage*current / 1000000,
                    cumpower
                )
                count = 0

if __name__ == '__main__':
    mp.set_start_method('spawn')

    manager = mp.Manager()
    q = manager.Queue()

    p = mp.Process(target=producer, args=(q, ))
    c = mp.Process(target=consumer, args=(q, ))

    p.start()
    c.start()

    p.join()
    c.join()
