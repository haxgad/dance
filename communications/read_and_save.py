from UART_client import UARTClient
from pprint import pprint
from csv import writer

if __name__ == "__main__":
    serial_port = '/dev/ttyAMA0'
    # serial_port = '/dev/ttyS0'

    client = UARTClient(serial_port)
    client.handshake()

    # Infinite loop
    index = 0
    with open('output.txt', 'rb') as csv_file:
        writer_obj = csv.writer(csv_file)
        try:
            while 1:
                data_list, error = client.receive_serialized_data()
                print("Index: {}".format(index))
                index += 1
                writer_obj.writerow(data_list)
        except KeyboardInterrupt:
            break
