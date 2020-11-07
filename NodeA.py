import socket
from AESFunctions import BLOCK_SIZE, encrypt_msg, decrypt_msg, string_xor

init_vector = "zaiilwo2y80d5ijo"
K3 = b'C2NsERGsOwGsV7PW'
# encrypt_mode = "ECB".encode('utf-8')
encrypt_mode = "OFB".encode('utf-8')
KM_PORT = 65432
B_PORT = 65433

if __name__ == "__main__":
    print("Starting Node A.")

    b_conn = socket.socket()
    b_conn.connect(('127.0.0.1', B_PORT))
    b_conn.send(encrypt_mode)
    print('Succesfully connected to Node B.')

    km_conn = socket.socket()
    km_conn.connect(('127.0.0.1', KM_PORT))
    km_conn.send(bytes(encrypt_mode))
    print('Succesfully connected to Node KM.')
    encrypted_key = km_conn.recv(BLOCK_SIZE)
    km_conn.close()

    key = decrypt_msg(encrypted_key, K3)
    print("Decrypted key is:", key)
    
    b_rdy = b_conn.recv(3)
    if(b_rdy == b"RDY"):
        print("Sending blocks to Node B.")
        with open('plaintext.txt', 'rb') as file:
            if encrypt_mode == b"ECB":
                block = file.read(BLOCK_SIZE)
                while len(block) != 0:
                    encrypted_block = encrypt_msg(block, key)
                    b_conn.send(encrypted_block)
                    block = file.read(BLOCK_SIZE)

            elif encrypt_mode == b"OFB":
                block = file.read(BLOCK_SIZE)
                while len(block) != 0:
                    init_vector = encrypt_msg(init_vector, key)
                    encrypted_block = string_xor(block, init_vector)
                    b_conn.send(encrypted_block)
                    block = file.read(BLOCK_SIZE)

    b_conn.close()