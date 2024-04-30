import socket
import threading

def handle_clients(client, addr):
    print(f'client address: {address}')

host = '0.0.0.0'
port = 8080
server = socket.socket()
server.bind((host, port))
server.listen(5)

print(socket.gethostbyname(socket.gethostname()))

threads = []

while True:
    (client_socket, address) = server.accept()
    
    t = threading.Thread(target=handle_clients, args=(client_socket, address))
    t.start()
    
    threads.append(t)
