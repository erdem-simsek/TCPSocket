# client program
import socket
import time

#IP address
HOST = '127.1.1.1'
PORT = 6007
#Create a sockets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))

while 1:
    message = input("Enter the desired operation \n")

    #send the desired operation to proxy
    client_socket.sendall(bytes(message,'utf-8'))
    time.sleep(0.5)

    #get a byte object with utf-8 encoding
    dataReceived=client_socket.recv(1024)
    #Decode the data into a string
    dataReceived = dataReceived.decode('utf-8')
    print("Operation is done.")
    print(dataReceived)
