import serial


class UARTClient:
    def __init__(self, port):
        self.ser = serial.Serial(port=port, baudrate=9600, timeout=3)
        self.ser.flush()

    def close(self):
        self.ser.close()

    def receive(self):
        try:
            line = self.ser.readline()
            line_prt = line.decode('utf-8').strip()
        except Exception as exc:
            return None, str(exc)

        # Return received message + error message
        return line_prt, None

    def receive_serialized_data(self):
        checksum = 0
        readings = []

        # Read the packet's size
        first_byte = self.ser.read()
        # # second_byte = self.ser.read()
        packet_size = int.from_bytes(first_byte, byteorder='big', signed=True)

        # Hardcode the packet's size
        packet_size = 19
        for _ in iter(range(packet_size)):
            first_byte = self.ser.read()
            second_byte = self.ser.read()
            value = int.from_bytes(second_byte + first_byte, byteorder='big', signed=True)
            readings.append(value)
            checksum ^= int.from_bytes(first_byte, byteorder='big', signed=True)
            checksum ^= int.from_bytes(second_byte, byteorder='big', signed=True)

        # Read the checksum
        first_byte = self.ser.read()
        second_byte = self.ser.read()
        package_checksum = int.from_bytes(second_byte + first_byte, byteorder='big', signed=True)

        print("\nChecksum calculated: {}".format(checksum))
        print("Checksum package: {}".format(package_checksum))

        # Return received message + error message
        return readings, None

    def send(self, message):
        if isinstance(message, str):
            message = message.encode('utf-8')

        try:
            self.ser.write(message)
            return
        except Exception as exc:
            return str(exc)

    def handshake(self):
        # Send a `start` message through Serial
        error = None
        while 1:
            error = self.send('1')
            if error is not None:
                print("ERROR:", error)
                continue
            break

        # Receive an `ack` message from Serial
        while 1:
            received_msg, error = self.receive()
            if error is not None:
                print("ERROR:", error)
            elif received_msg == 'ACK':
                break
            else:
                print("Expected to receive a text 'ACK', but instead got {}".format(repr(received_msg)))

        print('Handshake successfully.')

if __name__ == "__main__":
    serial_port = '/dev/ttyAMA0'
    # serial_port = '/dev/ttyS0'

    client = UARTClient(serial_port)
    client.handshake()
