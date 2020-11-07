import socket
from AESFunctions import BLOCK_SIZE, encrypt_msg, decrypt_msg, string_xor

init_vector = "zaiilwo2y80d5ijo"
K3 = b'C2NsERGsOwGsV7PW'
KM_PORT = 65432
B_PORT = 65433


print("Starting Node B.")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', B_PORT))
server.listen()

client, address = server.accept()
encrypt_mode = client.recv(3)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as km_conn:
    km_conn.connect(('127.0.0.1', KM_PORT))
    km_conn.send(bytes(encrypt_mode))
    encrypted_key = km_conn.recv(BLOCK_SIZE)

key = decrypt_msg(encrypted_key, K3)
print("Decrypted key is:", key)
client.send(b"RDY")

decrypted_msg = ""

if encrypt_mode == b"ECB":
    encrypted_block = client.recv(BLOCK_SIZE)
    while len(encrypted_block) != 0:
        decrypted_block = decrypt_msg(encrypted_block, key)
        decrypted_msg += decrypted_block
        encrypted_block = client.recv(BLOCK_SIZE)

elif encrypt_mode == b"OFB":
    encrypted_block = client.recv(BLOCK_SIZE)
    while len(encrypted_block) != 0:
        init_vector = encrypt_msg(init_vector, key)
        decrypted_block = string_xor(encrypted_block, init_vector)
        decrypted_msg += decrypted_block.decode("utf-8")
        encrypted_block = client.recv(BLOCK_SIZE)

print(decrypted_msg)
with open("decrypted.txt", 'w') as file:
    print(decrypted_msg, file = file, end="")

server.close()