

server = tcpserver("127.2.2.2",6009,"Timeout",20);
Data=[7,8,9,10,11,6,5,4,3,2];


while  1
   
    x=server.Connected
    if server.Connected
        operation = read(server);
        % operation data is in this format (W;1;5) (Write or Read; index;data)
        operation_split = split(operation,["=",";"]);
        index= str2num(operation_split(2));
        if operation_split(1)=="W"
            Data(index)=str2num(operation_split(3));
            end
        if operation_split(1)=="R";
            senddata=Data(index);
            write(server,senddata,"integer");
            end
        if operation_split(1)=="C"
            Data=[0,0,0,0,0,0,0,0,0,0];
            end
    end
end    
    

           
