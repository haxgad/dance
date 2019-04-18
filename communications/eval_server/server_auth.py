from Crypto.Cipher import AES
from Crypto import Random
import base64
import sys
import os


class ServerAuth:
    def __init__(self):
        super(ServerAuth, self).__init__()

    def compress_data_to_text(self, action, voltage, current, power, cumpower):
        allowed_sizes = (8, 16, 32, 64, 128, 256)
        output = "#{}|{}|{}|{}|".format(
                action,
                voltage,
                current,
                power)

        for size in allowed_sizes:
            if len(output) + len(str(cumpower)) <= size:
                num_zeros = '0' * (size - len(output) - len(str(cumpower)))
                cumpower =  num_zeros + str(cumpower)
                break

        output += cumpower
        return output


    def encrypt_text(self, raw_text, secret_key):
        # Cryto.Random is used instead of `os.urandom()`
        # because, a report in 2006 (https://en.wikipedia.org/wiki//dev/random)
        # states that `os.urandom()` has several issues with embedded and LIVE CD systems.
        # More about Crypto.Random's implementation: https://www.dlitz.net/software/pycrypto/doc/#crypto-random
        iv = Random.new().read(AES.block_size)

        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        cipher_text = cipher.encrypt(raw_text)
        return base64.b64encode(iv + cipher_text)

    def decrypt_text(self, cipherText, Key):
        decodedMSG = base64.b64decode(cipherText)
        # print(decodedMSG)
        iv = decodedMSG[:16]
        # print(iv)
        # secret_key = bytes(str(Key), encoding = "utf8")
        secret_key = Key
        # secret_key = base64.b64decode(Key)
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        decryptedText = cipher.decrypt(decodedMSG[16:]).strip()
        decryptedTextStr = decryptedText.decode('utf8')
        # decryptedTextStr1 = decryptedTextStr[decryptedTextStr.find('#'):]
        # decryptedTextFinal = bytes(decryptedTextStr1[1:],'utf8').decode('utf8')
        decryptedTextFinal = decryptedTextStr
        action = decryptedTextFinal.split('|')[0]
        voltage = decryptedTextFinal.split('|')[1]
        current = decryptedTextFinal.split('|')[2]
        power = decryptedTextFinal.split('|')[3]
        cumpower = decryptedTextFinal.split('|')[4]
        return {'action': action, 'voltage': voltage, 'current': current, 'power': power, 'cumpower': cumpower}
