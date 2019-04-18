import asyncio
import logging
from csv import writer
import sys
import logging
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

async def producer(myQueue):
    # Init producer
    logger = create_logger('root')
    client = UARTClient('/dev/ttyAMA0')
    buffer = []
    BUF_SIZE = 50
    index = 0

    # Get filename to output data
    # count = 0
    # prefix_name = '/home/pi/comms/output'
    # while os.path.isfile(prefix_name + str(count) + '.txt'):
    #     count += 1
    # filename = prefix_name + str(count) + '.txt'
    print('Producer ready')

    while 1:
        data_list, error = client.receive_serialized_data()
        # ToDo: Log power later

        if error:
            logger.error(str(error))
            continue

        if data_list:
            buffer.append((data_list[:15], data_list[15:]))
            logger.info("Index: {}".format(index))
            index += 1

        if len(buffer) >= BUF_SIZE:
            await q.put(buffer)

            # Clear the buffer for new data
            #buffer = buffer[BUF_SIZE/2:]
            buffer = []

async def consumer(q):
    logger = create_logger('ML', '/home/pi/comms/ml_output.log')
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
    buffer = []
    index = 0

    # Get filename to output data
    count = 0
    prefix_name = '/home/pi/comms/output'
    while os.path.isfile(prefix_name + str(count) + '.txt'):
        count += 1
    filename = prefix_name + str(count) + '.txt'

    clf = Classifier('/home/pi/dance/communications/window50_model.sav')
    print('Consumer ready')

	while 1:
		item = await q.get()
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

if __name__ == '__main__':
	# Global variables
    loop = asyncio.get_event_loop()
    q = asyncio.Queue(loop=loop)

    try:
        loop.run_until_complete(
            asyncio.gather(
                producer(q),
                consumer(q)
            )
        )
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
