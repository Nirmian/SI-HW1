# encrypt and decrypt from https://pycryptodome.readthedocs.io/en/latest/src/examples.html
from Crypto.Cipher import AES

BLOCK_SIZE = 16

def padding(text, bl_size):
    if(len(text) % bl_size != 0):
        if isinstance(text, (bytes, bytearray)):
            text = text.decode("utf-8")
        padding_length =  bl_size - len(text) % bl_size
        text = text + padding_length * chr(0)
    if isinstance(text, bytes):
        return text
    else:
        return text.encode("utf-8")

def encrypt_msg(text, key):
    cipher = AES.new(padding(key, BLOCK_SIZE), AES.MODE_ECB)
    encrypted_text = cipher.encrypt(padding(text, BLOCK_SIZE))
    return encrypted_text

def decrypt_msg(text, key):
    cipher = AES.new(padding(key, BLOCK_SIZE), AES.MODE_ECB)
    return cipher.decrypt(text).decode("utf-8")

def string_xor(s1, s2):
    return bytes([_a ^ _b for _a, _b in zip(s1, s2)])