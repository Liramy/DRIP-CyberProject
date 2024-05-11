import json
import socket
import threading
from ArticleScrapping import ArticleScrapper
from os import path
import sys
import os

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
    user_key = load_key()
    encoded_message = user_data.encode()
    f = Fernet(user_key)
    return f.encrypt(encoded_message)
    
def decrypt_user_data(encoded_user_data):
    """
    Decrypt given data
    """
    user_key = load_key()
    f = Fernet(user_key)
    decoded_mesage = f.decrypt(encoded_user_data)
    return decoded_mesage.decode()

# Function to create a database and table
def create_table():
    conn = sqlite3.connect('Server/users.db')  # Connect to or create the database
    c = conn.cursor()  # Create a cursor object to execute SQL commands

    # Create a table named 'users' with columns 'id', 'name', and 'password'
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, name TEXT, Password TEXT)''')

    conn.commit()  # Commit changes
    conn.close()   # Close connection

# Function to insert a user into the database
def insert_user(name, password):
    conn = sqlite3.connect('Server/users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, password))
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
    
def encrypt_obj(obj, cipher_suite):
        """Function for encrypting an object

        Args:
            obj (any): An object that you wish to transfer in sockets

        Returns:
            bytes: transferable string encrypted
        """
        serialized_obj = json.dumps(obj).encode()
        encrypted_obj = cipher_suite.encrypt(serialized_obj)
        return encrypted_obj

def decrypt_obj(enc, cipher_suite):
    """Function for decrypting an object

    Args:
        enc (bytes): Encrypted byte of an object

    Returns:
        any: Decrypted
    """
    decrypted_obj = cipher_suite.decrypt(enc)
    deserialized_obj = json.loads(decrypted_obj.decode())
    return deserialized_obj

def handle_clients(client:socket.socket, addr, cipher_suite):
    data = client.recv(4096)
    var = decrypt_obj(data, cipher_suite=cipher_suite)#pickle.loads(data)
    
    key = ''
    for varkey in var:
        key = varkey
    
    users = get_users()
        
    if key == 'Log in':
        for user in users:
            if decrypt_user_data(user[1]) == (var[key][0]) and decrypt_user_data(user[2]) == (var[key][1]):
                client.send("Valid".encode('utf-8'))
                handle_clients(client=client, addr=addr, cipher_suite=cipher_suite)
                return
        client.send("Invalid".encode('utf-8'))
        handle_clients(client=client, addr=addr, cipher_suite=cipher_suite)
        
    elif key == 'Register':
        insert_user(encrypt_user_data(var[key][0]), encrypt_user_data(var[key][1]))
        client.send("Valid".encode('utf-8'))
        handle_clients(client=client, addr=addr, cipher_suite=cipher_suite)
    elif key == 'Search':
        (subject, date) = (var[key])
        try:
            scrapper = ArticleScrapper(subject=subject, period=date, 
                                    max_results=25, language='En')
            send_data = encrypt_obj(scrapper.get_results(), cipher_suite)#pickle.dumps(scrapper.get_results())
        except:
            send_data = encrypt_obj("Too many requests")
        client.send(send_data)
    else:
        client.send("Invalid".encode('utf-8'))
        handle_clients(client=client, addr=addr, cipher_suite=cipher_suite)
        
create_table()
    
host = '0.0.0.0'
port = 8080
server = socket.socket()
server.bind((host, port))
server.listen(5)

print(socket.gethostbyname(socket.gethostname()))

threads = []
if not path.exists("chat-key.key"):
            key = Fernet.generate_key()
            if not path.exists("chat-key.key"):
                with open("chat-key.key", "wb") as key_file:
                    key_file.write(key)
else:
    key = open("chat-key.key", "rb").read()

cipher_suite = Fernet(key)

while True:
    (client_socket, address) = server.accept()
    
    t = threading.Thread(target=handle_clients, args=(client_socket, address, cipher_suite))
    t.start()
    
    threads.append(t)
