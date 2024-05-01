import pickle
import socket
import threading
from ArticleScrapping import ArticleScrapper

import sqlite3

# Function to create a database and table
def create_table():
    conn = sqlite3.connect('Server/users.db')  # Connect to or create the database
    c = conn.cursor()  # Create a cursor object to execute SQL commands

    # Create a table named 'users' with columns 'id', 'name', and 'password'
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (name TEXT, password TEXT)''')
    conn.commit()
    conn.close()

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
    conn.commit()
    conn.close()
    return users

def handle_clients(client:socket.socket, addr):
    data = client.recv(4096)
    var = pickle.loads(data)
    
    key = ''
    for varkey in var:
        key = varkey
    
    users = get_users()
        
    if key == 'Log in':
        for user in users:
            if user[0] == var[key][0] and user[1] == var[key][1]:
                client.send("Valid".encode('utf-8'))
                handle_clients(client=client, addr=addr)
                return
        client.send("Invalid".encode('utf-8'))
        handle_clients(client=client, addr=addr)
        
    elif key == 'Register':
        insert_user(var[key][0], var[key][1])
        client.send("Valid".encode('utf-8'))
        handle_clients(client=client, addr=addr)
    elif key == 'Search':
        (subject, date) = (var[key])
        scrapper = ArticleScrapper(subject=subject, period=date, 
                                   max_results=25, language='En')
        send_data = pickle.dumps(scrapper.get_results())
        print("Start sending")
        print(len(send_data))
        client.send(send_data)
    else:
        client.send("Invalid".encode('utf-8'))
        handle_clients(client=client, addr=addr)
        

create_table()

# Get all users and print them
users = get_users()
for user in users:
    print(user)
    
    
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
