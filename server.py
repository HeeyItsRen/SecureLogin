import sqlite3
import hashlib
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))

server.listen()

def receive():
    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_connection, args=(client,))
        thread.start()    

def login(client):
    client.send("username".encode())
    username = client.recv(1024).decode()
    client.send("password".encode())
    password = client.recv(1024)
    password = hashlib.sha256(password).hexdigest()

    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))
    
    if cur.fetchall():
        client.send("Login Successful".encode())
    else:
        client.send("Login Failed".encode())

def register(client):
    client.send("request Username".encode())
    username = client.recv(1024).decode()
    client.send("username received, requesting password".encode())
    password = client.recv(1024)
    hashpassword = hashlib.sha256(password).hexdigest()
    client.send("password received".encode())
    
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS userdata (
                    id INTEGER PRIMARY KEY,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL)""")
    try:
        cur.execute("SELECT * FROM userdata WHERE username = ?", (username,))
        duplicate = cur.fetchone()
        if duplicate is None:
            cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, hashpassword))
            conn.commit()
            client.send("Registration Successful".encode())
        else:
            print("Duplicate Username")
            client.send("Registration Failed".encode())
    except Exception as e:
         print('Exception: {}'.format(e))
         raise Exception(e)
         
    
def handle_connection(client):
    while True:
        msg = client.recv(1024).decode()
        if msg == "Login":
            login(client)
        elif msg == "Register":
            register(client)
        
        
receive()