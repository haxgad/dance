from UART_client import UARTClient
from pprint import pprint
from csv import writer
import logging
# from logger import create_logger

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

if __name__ == "__main__":
    serial_port = '/dev/ttyAMA0'
    # serial_port = '/dev/ttyS0'

    logger = create_logger('writer')
    client = UARTClient(serial_port)
    client.handshake()

    # Infinite loop
    index = 0
    while 1:
        with open('/home/pi/comms/output.txt', 'a') as csv_file:
            writer_obj = writer(csv_file)
            data_list, error = client.receive_serialized_data()
            # print("Index: {}".format(index))
            logger.info("Index: {}".format(index))
            index += 1
            writer_obj.writerow(data_list)
