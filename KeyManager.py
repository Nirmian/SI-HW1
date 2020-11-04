import socket
from AESFunctions import encrypt_msg

K1 = b'K1'
K2 = b'K2'
K3 = b'K3'
HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    print("Starting Key Manager")
    server.bind((HOST, PORT))
    server.listen()
    while True:
        client, address = server.accept()
        print('Server listening on', (HOST, PORT))
        data = client.recv(1024).decode()
        encrypted_key = b''

        if data == "ECB":
            encrypted_key = encrypt_msg(K1, K3)
        
        elif data == "OFB":
            encrypted_key = encrypt_msg(K2, K3)

        client.send(encrypted_key)