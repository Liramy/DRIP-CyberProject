import socket
import ip_login
from LoginApp import LoginApp
from App import App
from os import path
from cryptography.fernet import Fernet

def socket_connect(ip, port):
    client_socket.connect((ip, port))

if not path.exists("../chat-key.key"):
    key = Fernet.generate_key()
    if not path.exists("../chat-key.key"):
        with open("../chat-key.key", "wb") as key_file:
            key_file.write(key)
else:
    key = open("../chat-key.key", "rb").read()
    
print(key)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_app = ip_login.IP_Login(socket_connect)
IP_app.mainloop()
    
login_app = LoginApp(client_socket, key)
login_app.mainloop()

main_app = App(client_socket, key)
main_app.mainloop()
