import socket
from threading import Thread    
import os

client = socket.socket()
client.connect(('localhost', 9999))

name = input('Enter your name: ')

def send(client):
    while True:
        message = input(" Enter your message (or type 'filename' to send a file): ")
        # data = f'{name}:{input(" ")}'

        if(message =='filename'):
            filename = input("Enter the filename: ")
            if os.path.exists(filename):
                with open(filename, 'rb') as file:
                    file_data = file.read()
                    client.send(f'file:{filename}:{len(file_data)}'.encode('utf-8'))
                    client.send(file_data)
                    print(f'Sent file: {filename}')
        else:
            data = f'{name}:{message}'
            client.send(data.encode('utf-8'))
            


    

def receive(client):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if(msg.startswith('file:')):
                filename, filesize = msg.split(':')[1:]
                filesize = int(filesize)

                with open(f"received_{filename}", 'wb') as file:
                    received = 0
                    while received < filesize:
                        f_data = client.recv(1024)
                        if not f_data:
                            break
                        file.write(f_data)
                        received += len(f_data)
                print(f'File {filename} received successfully.')

            else:
                print(msg)            
        except:
            client.close()
            break

thread1 = Thread(target=send, args=(client,))
thread1.start()
thread2 = Thread(target=receive, args=(client,))
thread2.start()