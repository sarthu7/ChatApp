import socket
from threading import Thread

server = socket.socket()
server.bind(('localhost', 9999))

server.listen()
all_clients = {}

def client_thread(client):
    while True:   
        try:

            msg = client.recv(1024)
            
            if msg.startswith(b'file:'):
                msg = msg.decode('utf-8')
                filename,filesize = msg.split(':')[1:]
                filesize = int(filesize)

                for c in all_clients:
                    if c!= client:
                        c.send(msg.encode('utf-8'))

                received = 0
                while received < filesize:
                    file_data = client.recv(1024)
                    received += len(file_data)
                    for c in all_clients:
                        if c != client:
                            c.send(file_data)

            else:
                for c in all_clients:
                    if c != client:
                        c.send(msg)  

        except Exception as e:
            client.close()
            del all_clients[client]
        

while True:
    print('Waiting for connection...')

    client, addr = server.accept()
    print("connection established with", addr)

    name = client.recv(1024).decode()

    all_clients[client] = name

    thread = Thread(target=client_thread,args=(client,))
    thread.start()


