import socket
import ip_login
from LoginApp import LoginApp
from App import App
from os import path
import os
from cryptography.fernet import Fernet
import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
import json

def socket_connect(ip, port):
    client_socket.connect((ip, port))

def load_key():
        key_path = "public_key.pem"
        file_exists = path.exists(key_path)
        if file_exists:
            with open(key_path, "rb") as f:
                return serialization.load_pem_public_key(f.read())
        print("Error - no key found")
        return None
    
def start_connection(sock:socket.socket, public_key, symmetric_key):
    encrypted_request = encrypt_obj(symmetric_key, public_key)
    sock.send(encrypted_request)
    
def encrypt_obj(obj, key):
    encrypt_obj = key.encrypt(
        obj,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypt_obj


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
public_key = load_key()
symmetric_key = os.urandom(32)

IP_app = ip_login.IP_Login(socket_connect)
IP_app.mainloop()

start_connection(client_socket, public_key, symmetric_key=symmetric_key)
    
login_app = LoginApp(client_socket, symmetric_key)
login_app.mainloop()

main_app = App(client_socket, symmetric_key)
main_app.mainloop()
