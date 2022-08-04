# instead of matlab filei it is written for trying

import socket
import time
import re
#Loopback IP address
HOST = '127.2.2.2'
PORT = 6009
#Create a sockets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket successfully created")

# This line avoids bind() exception: OSError: [Errno 48] Address already in use as you configure address reuse
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
print ("Socket is bound to IP:",HOST," PORT:",PORT)
server_socket.listen(1)
print("Listening for connections")
server, serverAddress = server_socket.accept()
print ('Connected to proxy')

Data=[7,8,9,10,11,6,5,4,3,2]
while 1:
    try:
        operation = server.recv(1024)
    except OSError:
        print (serverAddress, 'disconnected')
        server_socket.listen(1)
        conn, clientAddress = server_socket.accept()
        print ('Connected by', serverAddress)
        time.sleep(0.5)

    else:    
        #Decode the data into a string
        operation = operation.decode('utf-8')
        #split operation
        operation_split = re.split(';|,', operation)
         
        if operation_split[0]=='R':
            server.sendall(bytes(str(Data[int(operation_split[1])]),'utf-8'))
            
        if operation_split[0]=='W':
            Data[int(operation_split[1])]=int(operation_split[2])
            
        if operation_split[0]=='C':
           Data=[0,0,0,0,0,0,0,0,0,0]
           
           
           
           
           
           
           
           
           
           