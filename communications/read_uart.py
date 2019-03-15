from UART_client import UARTClient


if __name__ == "__main__":
    serial_port = '/dev/ttyAMA0'
    # serial_port = '/dev/ttyS0'

    client = UARTClient(serial_port)

    # Infinite loop
    index = 0
    while 1:
        message, error = client.receive()
        print("{}: {}".format(index, repr(message)))
        index += 1
