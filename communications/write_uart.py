from UART_client import UARTClient
from time import sleep

if __name__ == "__main__":
    serial_port = '/dev/ttyAMA0'
    # serial_port = '/dev/ttyS0'

    client = UARTClient(serial_port)

    index = 0
    while 1:
        # message = input('Enter text: ')
        message = "{}: {}".format(index, "testing")
        index += 1
        client.send(message)
        sleep(2)
