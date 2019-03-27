from UART_client import UARTClient
from timeit import default_timer

if __name__ == "__main__":
    serial_port = '/dev/ttyAMA0'
    # serial_port = '/dev/ttyS0'

    client = UARTClient(serial_port)
    client.handshake()
    # Infinite loop
    index = 0
    while 1:
        start = default_timer()
        message, error = client.receive()
        print("{}: {}".format(index, repr(message)))
        print(default_timer() - start)
        index += 1
