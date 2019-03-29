import socket
from logger import create_logger

from .server_auth import ServerAuth

class SocketClient:
    def __init__(self, ip_addr, port):
        self.logger = create_logger('SocketClient')
        self.secret_key = "randomstuff12345"
        # init server
        self.auth = ServerAuth()

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        self.server_address = (ip_addr, port)

    def connect(self):
        self.sock.connect(self.server_address)
        self.logger.info('Successfully connected to server')

    def close(self):
        self.sock.close()

    def send(self, message):
        print(message)
        encoded_msg = self.auth.encrypt_text(message, self.secret_key)
        self.sock.sendall(encoded_msg)
        self.logger.debug('Message sent')

    def send_data(self, action, voltage, current, power, cumpower):
        message = self.auth.compress_data_to_text(action, voltage, current, power, cumpower)
        self.send(message)
