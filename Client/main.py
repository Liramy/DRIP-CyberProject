import socket
import pickle
import ip_login
from LoginApp import LoginApp
from App import App

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_app = ip_login.IP_Login(client_socket)
IP_app.mainloop()
    
login_app = LoginApp(client_socket)
login_app.mainloop()

main_app = App(client_socket)
main_app.mainloop()
