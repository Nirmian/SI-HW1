import socket
from AESFunctions import BLOCK_SIZE, encrypt_msg, decrypt_msg, string_xor

init_vector = "zaiilwo2y80d5ijo"
K3 = b'K3'
KM_ADDRESS = '127.0.0.1'
KM_PORT = 65432
B_ADDRESS = '127.0.0.1'
B_PORT = 65433


print("Starting Node B.")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((B_ADDRESS, B_PORT))
server.listen()

client, address = server.accept()
ENCRYPT_MODE = client.recv(3)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as km_conn:
    km_conn.connect((KM_ADDRESS, KM_PORT))
    km_conn.send(bytes(ENCRYPT_MODE))
    encrypted_key = km_conn.recv(BLOCK_SIZE)

key = decrypt_msg(encrypted_key, K3)
print("Decrypted key:", key)
client.send(b"RDY")

decrypted_msg = ""
if ENCRYPT_MODE == b"ECB":
    encrypted_block = client.recv(BLOCK_SIZE)
    while len(encrypted_block) != 0:
        decrypted_block = decrypt_msg(encrypted_block, key)
        decrypted_block = decrypted_block.rstrip('\x00')
        decrypted_msg += decrypted_block
        encrypted_block = client.recv(BLOCK_SIZE)

elif ENCRYPT_MODE == b"OFB":
    encrypted_block = client.recv(BLOCK_SIZE)
    while len(encrypted_block) != 0:
        init_vector = encrypt_msg(init_vector, key)
        decrypted_block = string_xor(encrypted_block, init_vector)
        decrypted_msg += decrypted_block.decode("utf-8")
        encrypted_block = client.recv(BLOCK_SIZE)

print(decrypted_msg)
server.close()