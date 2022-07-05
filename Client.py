from socket import *
import os

server = ("localhost", 1500)
clientSocket = socket(AF_INET, SOCK_DGRAM)

PATH = os.path.dirname(__file__) + "\\Client\\"

if(not os.path.exists(PATH)):
    os.mkdir(PATH)

BUFFER = 1024
INIT_TEXT = "Choose one of this operations:\n- list\n- get <filename>\n- put <filename>"
C_ERROR_TEXT = "Command not found"
F_ERROR_TEXT = "File not found"

print("Open client")
while True:
    
    print(INIT_TEXT)
    
    fullCommand = input()
    command = fullCommand.split()[0]
    if (len(fullCommand) > len(fullCommand.split()[0]) + 1):
        fileName = fullCommand[4:]
    else:
        fileName = "?"
    if (command == "list"):
        clientSocket.sendto(command.encode(), server)
        fileList, address = clientSocket.recvfrom(BUFFER)
        print(fileList.decode())
        
    elif(command.split()[0] == "get"):
        clientSocket.sendto(command.encode(), server)
        clientSocket.sendto(fileName.encode(), server)
        line, address = clientSocket.recvfrom(BUFFER)
        if (line == F_ERROR_TEXT.encode()):
            print(F_ERROR_TEXT)
        else:
            writer = open(PATH + fileName, 'wb')
            writer.write(line)
            while line != b'':
                line, address = clientSocket.recvfrom(BUFFER)
                writer.write(line)
            writer.close()
            print("Download completed")
        
    elif(command.split()[0] == "put"):
        if (not os.path.exists(PATH + fileName)):
            print(F_ERROR_TEXT)
        else:
            clientSocket.sendto(command.encode(), server)
            clientSocket.sendto(fileName.encode(), server)
            reader = open(PATH + fileName, 'rb')
            buffer = reader.read(BUFFER)
            while buffer != b'':
                clientSocket.sendto(buffer, server)
                buffer = reader.read(BUFFER)
            clientSocket.sendto(b'', server)
            reader.close()
            print("Upload completed")
    else:
        print(C_ERROR_TEXT)
            