# Proxy program
import socket
import time
import re


#Connection for client-proxy
#IP address 
C_HOST = '127.1.1.1'
C_PORT = 6007

#Create sockets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Client socket successfully created")

# This line avoids bind() exception: OSError: [Errno 48] Address already in use as you configure address reuse
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.bind((C_HOST, C_PORT))
print ("Client socket is bound to IP:",C_HOST," PORT:",C_PORT)
client_socket.listen(1)
print("Listening for connections for client")
conn_client, clientAddress = client_socket.accept()
print ('Connected to client')


#Connection for proxy-server
#IP address 
S_HOST = '127.2.2.2'
S_PORT = 6009

#Create sockets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((S_HOST,S_PORT))
print ('Connected to server')

cached_table=[[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[1,2,3,4,5]] #2d array shows index, value and counter that indicates oldest value
data=[]

while 1:
    i=0
    sum_ind=0
    count=0
    flag_found=0
    smallest=5
    smallest_index=0
    a=0
    try:
        operation = conn_client.recv(1024)
        
    except OSError:
        print (clientAddress, 'disconnected')
        client_socket.listen(1)
        conn_client, clientAddress = client_socket.accept()
        print ('Connected by', clientAddress)
        time.sleep(0.5)

    else:    

        #Decode the data into a string
        operation = operation.decode('utf-8')
        #split operation
        dataSplit = re.split(';|=', operation)
        
        if dataSplit[1]=='GET': #perform get operation
            indices = re.split(',|;', dataSplit[3])
            response_to_client='OP=GET;IND='+dataSplit[3]+';DATA='
            
            
            for x in indices:
                while i<5:
                    if cached_table[0][i]==int(x):
                        response_to_client += str(cached_table[1][i]) +','
                        flag_found=1
                        break
                    i+=1
                    
                
                if flag_found==0:
                    message="R;"+x+";0;"
                    server_socket.sendall(bytes(message,'utf-8'))
                    time.sleep(1)
                    dataReceived=server_socket.recv(1024)
                    dataReceived = dataReceived.decode('utf-8')
                    i=0
                    while i<5:# determine oldest value, oldest means smallest
                        if smallest>cached_table[2][i]:
                            smallest=cached_table[2][i]
                            smallest_index=i
                        i+=1
                    
                    cached_table[1][smallest_index]=int(dataReceived)
                    cached_table[0][smallest_index]=int(x)
                    cached_table[2][smallest_index]=5 #set oldest value as newest one
                    i=0
                    while i<5:
                        if smallest_index!=i:#other indexes decremented 1 
                            cached_table[2][i]-=1
                        i+=1
                    response_to_client += str(cached_table[1][smallest_index]) +','  
            response_to_client+=';'
            
        elif dataSplit[1]=='PUT':
            indices = re.split(',|;', dataSplit[3])
            data= re.split(',|;', dataSplit[5])
            
            for x in indices:
                while i<5:
                    if cached_table[0][i]==int(x): # if index matched with cached table 
                        cached_table[1][i]=int(data[a])
                        flag_found=1
                        break
                    i+=1
                
                if flag_found==0: #if there is no matched with indexes put the data to oldest value
                    i=0
                    while i<5:# determine oldest value, oldest means smallest
                        if smallest>cached_table[2][i]:
                            smallest=cached_table[2][i]
                            smallest_index=i
                        i+=1
                    cached_table[1][smallest_index]=int(data[a])
                    message="W;"+str(smallest_index)+";"+data[a]+";"
                    server_socket.sendall(bytes(message,'utf-8'))
                    time.sleep(0.5)
                    cached_table[2][smallest_index]=5 #set oldest value as newest one
                    i=0
                    while i<5:
                        if smallest_index!=cached_table[0][i]:#other indexes decremented 
                            cached_table[2][i]-=1
                        i+=1
                a+=1
            response_to_client='PUT is done'
            
        elif dataSplit[1]=='CLR': 
            cached_table=[[0,1,2,3,4],[0,0,0,0,0],[1,2,3,4,5]]
            server_socket.sendall(bytes("C;",'utf-8'))
            response_to_client='CLR is done'
            
        elif dataSplit[1]=='ADD': 
            indices = re.split(',', dataSplit[3])
            response_to_client='OP=ADD;IND='+dataSplit[3]+';DATA='
            
            for x in indices:
                while i<5:
                   if cached_table[0][i]==int(x):
                       sum_ind += cached_table[1][i]
                       flag_found=1
                       break
                   i+=1
                   
                if flag_found==0:
                     server_socket.sendall(bytes("R;"+x+";0;",'utf-8'))
                     time.sleep(0.5)
                     dataReceived=server_socket.recv(1024)
                     dataReceived = dataReceived.decode('utf-8')
                     i=0
                     while i<5:# determine oldest value, oldest means smallest
                         if smallest>cached_table[2][i]:
                             smallest=cached_table[2][i]
                             smallest_index=i
                         i+=1
                     cached_table[1][smallest_index]=int(dataReceived)
                     cached_table[0][smallest_index]=int(x)
                     cached_table[2][smallest_index]=5 #set oldest value as newest one
                     i=0
                     while i<5:
                         if smallest_index!=i:#other indexes decremented 1 
                             cached_table[2][i]-=1
                         i+=1
                     sum_ind += cached_table[1][smallest_index] 
            
            response_to_client += str(sum_ind) +';'
            
        elif dataSplit[1]=='AVG': 
            indices = re.split(',', dataSplit[3])
            response_to_client='OP=AVG;IND='+dataSplit[3]+';DATA='
            
            for x in indices:
                while i<5:
                   if cached_table[0][i]==int(x):
                       sum_ind += cached_table[1][i]
                       count+=1
                       flag_found=1
                       break
                   i+=1
                   
                if flag_found==0:
                     server_socket.sendall(bytes("R;"+x+";0;",'utf-8'))
                     time.sleep(0.5)
                     dataReceived=server_socket.recv(1024)
                     dataReceived = dataReceived.decode('utf-8')
                     i=0
                     while i<5:# determine oldest value, oldest means smallest
                         if smallest>cached_table[2][i]:
                             smallest=cached_table[2][i]
                             smallest_index=i
                         i+=1
                     cached_table[1][smallest_index]=int(dataReceived)
                     cached_table[0][smallest_index]=int(x)
                     cached_table[2][smallest_index]=5 #set oldest value as newest one
                     i=0
                     while i<5:
                         if smallest_index!=i:#other indexes decremented 1 
                             cached_table[2][i]-=1
                         i+=1
                     sum_ind += cached_table[1][smallest_index]
                     count+=1
            
            response_to_client += str(float(sum_ind)/float(count)) +';'    
    
        else :
            response_to_client ='Invalid operation'
        #Encode and send the data back to the client
        conn_client.sendall(bytes(response_to_client,'utf-8'))
        

