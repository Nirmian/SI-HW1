import socket
from AESFunctions import BLOCK_SIZE, aes_encrypt, aes_decrypt

INIT_VECTOR = "zaiilwo2y80d5ijo"
K3 = b'K3'
ENCRYPT_MODE = "ECB".encode('utf-8')
# ENCRYPT_MODE = "OFB".encode('utf-8')
KM_ADDRESS = '127.0.0.1'
KM_PORT = 65432
B_ADDRESS = '127.0.0.1'
B_PORT = 65433


if __name__ == "__main__":
    b_conn = socket.socket()
    b_conn.connect((B_ADDRESS, B_PORT))
    b_conn.send(ENCRYPT_MODE)
    print('Succesfully connected to Node B.')

    km_conn = socket.socket()
    km_conn.connect((KM_ADDRESS, KM_PORT))
    km_conn.send(bytes(ENCRYPT_MODE))
    print('Succesfully connected to Node KM.')
    encrypted_key = km_conn.recv(BLOCK_SIZE)
    km_conn.close()

    key = aes_decrypt(encrypted_key, K3)
    print("Decrypted key:", key)
    
    b_rdy = b_conn.recv(3)
    if(b_rdy == b"RDY"):
        print("Sending blocks to Node B.")
        with open('plaintext.txt', 'rb') as file:
            if ENCRYPT_MODE == b"ECB":
                block = file.read(BLOCK_SIZE)
                while len(block) != 0:
                    encrypted_block = aes_encrypt(block, key)
                    b_conn.send(encrypted_block)
                    block = file.read(BLOCK_SIZE)

            elif ENCRYPT_MODE == b"OFB":
                print("OFB MODE")

    b_conn.close()