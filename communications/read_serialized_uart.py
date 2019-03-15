from UART_client import UARTClient
from pprint import pprint

if __name__ == "__main__":
    serial_port = '/dev/ttyAMA0'
    # serial_port = '/dev/ttyS0'

    client = UARTClient(serial_port)
    client.handshake()

    # Infinite loop
    index = 0
    while 1:
        message, error = client.receive_serialized_data()
        # print("{}: {}".format(index, repr(message)))
        # print("{}: ".format(index), end='')
        print(index)
        print(message)
        index += 1
