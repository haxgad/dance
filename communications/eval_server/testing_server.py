from time import sleep

from server_auth import ServerAuth
from socket_client import SocketClient

key="randomstuff12345"
raw_text = "raffles|31|5|7|9"

# actions
# voltage 3
# current 3
# power  = Cur * Voltage
# cumpower 5
auth = ServerAuth()

# cipher_text = auth.encrypt_text(raw_text, key)
# print(cipher_text)
#
# decoded_text = auth.decrypt_text(cipher_text, key)
# print(decoded_text)

socket_client = SocketClient('localhost', 8888)
socket_client.connect()

# Final_eval_server command:
# python final_eval_server_5moves.py localhost 8888 group_num_123

user_inp = ''
while 1:
    print('Input: ')
    user_inp = input()
    try:
        if user_inp == '1':
            # msg = auth.encrypt_text(raw_text, key)
            socket_client.send(raw_text)
            print('sent')
            print()
        elif user_inp == '2':
            break
    except KeyboardInterrupt:
        break
