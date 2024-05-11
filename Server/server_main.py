from EncMethod import Kdot
import socket
import threading
from ArticleScrapping import ArticleScrapper
from os import path

import sqlite3

from cryptography.fernet import Fernet
import base64

def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    if not path.exists("Server/secret.key"):
        with open("Server/secret.key", "wb") as key_file:
            key_file.write(key)

def load_key():
    """
    Load the previously generated key
    """
    if not path.exists("Server/secret.key"):
        generate_key()
    return open("Server/secret.key", "rb").read()

def encrypt_user_data(user_data):
    """
    Encrypts a message
    """
    key = load_key()
    encoded_message = user_data.encode()
    f = Fernet(key)
    return f.encrypt(encoded_message)
    
def decrypt_user_data(encoded_user_data):
    """
    Decrypt given data
    """
    key = load_key()
    f = Fernet(key)
    decoded_mesage = f.decrypt(encoded_user_data)
    return decoded_mesage.decode()

# Function to create a database and table
def create_table():
    conn = sqlite3.connect('Server/users.db')  # Connect to or create the database
    c = conn.cursor()  # Create a cursor object to execute SQL commands

    # Create a table named 'users' with columns 'id', 'name', and 'age'
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

    conn.commit()  # Commit changes
    conn.close()   # Close connection

# Function to insert a user into the database
def insert_user(name, age):
    conn = sqlite3.connect('Server/users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

# Function to get all users from the database
def get_users():
    conn = sqlite3.connect('Server/users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return users

# Function to clear all data from the 'users' table
def clear_users_table():
    conn = sqlite3.connect('Server/users.db')
    c = conn.cursor()
    c.execute("DELETE FROM users")
    conn.commit()
    conn.close()

def handle_clients(client:socket.socket, addr, kdot:Kdot):
    data = client.recv(4096)
    var = kdot.decrypt_obj(data)#pickle.loads(data)
    
    key = ''
    for varkey in var:
        key = varkey
    
    users = get_users()
        
    if key == 'Log in':
        for user in users:
            if decrypt_user_data(user[1]) == (var[key][0]) and decrypt_user_data(user[2]) == (var[key][1]):
                client.send("Valid".encode('utf-8'))
                handle_clients(client=client, addr=addr)
                return
        client.send("Invalid".encode('utf-8'))
        handle_clients(client=client, addr=addr)
        
    elif key == 'Register':
        insert_user(encrypt_user_data(var[key][0]), encrypt_user_data(var[key][1]))
        client.send("Valid".encode('utf-8'))
        handle_clients(client=client, addr=addr)
    elif key == 'Search':
        (subject, date) = (var[key])
        scrapper = ArticleScrapper(subject=subject, period=date, 
                                   max_results=25, language='En')
        send_data = kdot.encrypt_obj(scrapper.get_results())#pickle.dumps(scrapper.get_results())
        client.send(send_data)
    else:
        client.send("Invalid".encode('utf-8'))
        handle_clients(client=client, addr=addr)
        
        
create_table()
    
host = '0.0.0.0'
port = 8080
server = socket.socket()
server.bind((host, port))
server.listen(5)

print(socket.gethostbyname(socket.gethostname()))

threads = []
kdot = Kdot()

while True:
    (client_socket, address) = server.accept()
    
    t = threading.Thread(target=handle_clients, args=(client_socket, address, kdot))
    t.start()
    
    threads.append(t)
