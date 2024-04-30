import socket
import pickle
import ip_login
from LoginApp import LoginApp

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_IP = "26.58.20.252"
server_PORT = 8080

IP_app = ip_login.IP_Login(client_socket)
IP_app.mainloop()
    
login_app = LoginApp(client_socket)
login_app.mainloop()
