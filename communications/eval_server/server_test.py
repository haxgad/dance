import socket
from pprint import pprint
import sys

if __name__ == "__main__":
    ip_addr = 'localhost'
    port_num = 8889

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip_addr, port_num)

    print('starting up on %s port %s' % server_address, file=sys.stderr)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    # Wait for a connection
    print('waiting for a connection', file=sys.stderr)
    connection, client_address = sock.accept()
    while 1:
        data = self.connection.recv(1024)
        if data:
            msg = data.decode("utf8")
            decodedmsg = self.auth.decrypt_text(msg, secret_key)
            pprint(decodedmsg)
