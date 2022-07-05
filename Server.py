from socket import *
import os

server = ("localhost", 1500)
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(server)

PATH = os.path.dirname(__file__) + "\\Server\\"

if(not os.path.exists(PATH)):
    os.mkdir(PATH)

BUFFER = 1024

C_ERROR_TEXT = "Command not found"
F_ERROR_TEXT = "File not found"

print("Open server: ", server)
while True:
    command, address = serverSocket.recvfrom(BUFFER)
    command = command.decode()
    print("Executing:", command)
    if (command == "list"):
        output = ""
        for file in os.scandir(PATH):
            output += file.name + "\n"
        if (output == ""):
            output = "Empty list..."
        serverSocket.sendto(output.encode(), address)
        print("list executed")
        
    elif(command == "get"):
        fileName, address = serverSocket.recvfrom(BUFFER)
        if(not os.path.exists(PATH + fileName.decode())):
            print(F_ERROR_TEXT)
            serverSocket.sendto(F_ERROR_TEXT.encode(), address)
        else:
            reader = open(PATH + fileName.decode(), 'rb')
            buffer = reader.read(BUFFER)
            while buffer != b'':
                serverSocket.sendto(buffer, address)
                buffer = reader.read(BUFFER)
            serverSocket.sendto(b'', address)
            reader.close()
            print("File sent")
        
    else:
        fileName, address = serverSocket.recvfrom(BUFFER)
        writer = open(PATH + fileName.decode(), 'wb')
        reader, address = serverSocket.recvfrom(BUFFER)
        while reader != b'':
            writer.write(reader)
            reader, address = serverSocket.recvfrom(BUFFER)
        writer.close()
        print("File received")