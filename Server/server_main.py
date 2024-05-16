import json
import socket
import threading
from ArticleScrapping import ArticleScrapper
from os import path
import sys
import os

import sqlite3
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import b64encode, b64decode
from cryptography.hazmat.backends import default_backend

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
                 (id INTEGER PRIMARY KEY, name TEXT, password TEXT)''')

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
    
def encrypt_message(obj, symmetric_key):
    encrypted_message = json.dumps(obj).encode()
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(encrypted_message) + encryptor.finalize()

    payload = json.dumps({
        'iv': b64encode(iv).decode('utf-8'),
        'message': b64encode(encrypted_message).decode('utf-8')
    })
    return payload.encode()

def decrypt_obj(enc, symmetric_key):
    json_data = json.loads(enc)
    iv = b64decode(json_data['iv'])
    encrypted_msg = b64decode(json_data['message'])

    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend)
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_msg) + decryptor.finalize()
    return json.loads(decrypted_message)
    
def decrypt_key(enc, private_key):
    symmetric_key = private_key.decrypt(
    enc,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        )
    )
    return symmetric_key

def handle_start(client, address, private_key):
    data = client.recv(4096)
    key = decrypt_key(data, private_key)
    t = threading.Thread(target=handle_clients, args=(client, address, key))
    t.start()

def handle_clients(client:socket.socket, addr, symmetric_key):
    data = client.recv(4096)
    var = decrypt_obj(data, symmetric_key=symmetric_key)#pickle.loads(data)
    
    key = ''
    for varkey in var.keys():
        key = varkey
    
    users = get_users()
        
    if key == 'Log in':
        for user in users:
            if decrypt_user_data(user[1]) == (var[key][0]) and decrypt_user_data(user[2]) == (var[key][1]):
                client.send("Valid".encode('utf-8'))
                handle_clients(client=client, addr=addr, symmetric_key=symmetric_key)
                return
        client.send("Invalid".encode('utf-8'))
        handle_clients(client=client, addr=addr, symmetric_key=symmetric_key)
        
    elif key == 'Register':
        insert_user(encrypt_user_data(var[key][0]), encrypt_user_data(var[key][1]))
        client.send("Valid".encode('utf-8'))
        handle_clients(client=client, addr=addr, symmetric_key=symmetric_key)
    elif key == 'Search':
        (subject, date) = (var[key])
        try:
            scrapper = ArticleScrapper(subject=subject, period=date, 
                                    max_results=25, language='En')
            send_data = encrypt_message(scrapper.get_results(), symmetric_key)#pickle.dumps(scrapper.get_results())
        except:
            send_data = encrypt_message("Too many requests", symmetric_key)
        client.send(send_data)
    else:
        client.send("Invalid".encode('utf-8'))
        handle_clients(client=client, addr=addr, symmetric_key=symmetric_key)
        
def generate_key():
    """To be used only if key does not exist"""
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048)
    
def save_key(private_key):
    with open("Server/private_key.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )
        
def generate_public_key(private_key):
    public_key = private_key.public_key()
    with open("Server/public_key.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )
        
def load_private_key():
    private_key_path = "Server/private_key.pem"
    
    file_exists = path.exists(private_key_path)
    if file_exists:
        with open(private_key_path, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)
        
    print("Error - no key found")
    return None

def load_public_key():
    public_key_path = "Server/public_key.pem"
    
    file_exists = path.exists(public_key_path)
    if file_exists:
        with open(public_key_path, "rb") as f:
            return serialization.load_pem_public_key(f.read())
    print("Error - key not found")
    return None

    
host = '0.0.0.0'
port = 8080
server = socket.socket()
server.bind((host, port))
server.listen(5)
create_table()
print(socket.gethostbyname(socket.gethostname()))

threads = []
private_key = load_private_key()

while True:
    (client_socket, address) = server.accept()
    
    handle_start(client_socket, address, private_key)
