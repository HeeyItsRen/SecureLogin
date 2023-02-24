import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

# msg = client.recv(1024).decode()
client.send(input("username").encode())
# msg = client.recv(1024).decode()
client.send(input("password").encode())

print(client.recv(1024).decode())