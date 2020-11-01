from Crypto.Cipher import AES

BLOCK_SIZE = 16
NULL = chr(0)

# Text can't end with chr(0)
def padding(text):
    if(len(text) % BLOCK_SIZE != 0):
        if isinstance(text, (bytes, bytearray)):
            text = text.decode("utf-8")
        return (text + ((BLOCK_SIZE - len(text) % BLOCK_SIZE - 1)) * NULL + (chr(BLOCK_SIZE - len(text) % BLOCK_SIZE))).encode("utf-8")
    if isinstance(text, bytes):
        return text
    else:
        return text.encode("utf-8")

def aes_encrypt(text, key):
    key = padding(key)
    text = padding(text)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_text = cipher.encrypt(text)
    return encrypted_text

def aes_decrypt(text, key):
    key = padding(key)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(text).decode("utf-8")