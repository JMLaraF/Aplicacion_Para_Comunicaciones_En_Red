import os
import threading
import socket


class Server:
    def __init__(self):
        self.ip = ""
        self.port = 34567
        self.fSender = fileSender(self.ip , self.port-1)


    def listener(self):
        sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
        sock.bind((self.ip , self.port))
        while True:
            data , addr = sock.recvfrom(100)
            cmdArgs = data.decode('utf-8').split()
            print(cmdArgs[0])
            if(cmdArgs[0] == "RF"):
                fileInBytes = self.fSender.reciveFile(cmdArgs[2])
                sock.sendto(b'RTR' , addr)
                if(cmdArgs[2] == '0'):
                    leftSize = len(fileInBytes) // 3
                    rigthSize = 2*len(fileInBytes) // 3
                    xPart = fileInBytes[0:leftSize]
                    yPart = fileInBytes[leftSize+1:rigthSize]
                    zPart = fileInBytes[rigthSize+1:len(fileInBytes)]
                    sock.sendto(("RF 1 " + cmdArgs[2] + "_1").encode('utf-8'),(cmdArgs[3] , self.port))
                    sock.sendto(("RF 1 " + cmdArgs[2] + "_2").encode('utf-8'),(cmdArgs[4] , self.port))
                    sock.sendto(("RF 1 " + cmdArgs[2] + "_3").encode('utf-8'),(cmdArgs[5] , self.port))
                else:
                    writeFileOnSystem(fileInBytes , cmdArgs[2])
            elif(cmdArgs[0] == "GMF"):
                msg = "GMP " + cmdArgs[1] + "_1"
                sock.sendto(msg.encode('utf-8') , (cmdArgs[2] , self.port))
                ACK , addr = sock.recvfrom(100)
                data = ACK.decode('utf-8')
                xPart = self.fSender.reciveFile(cmdArgs[1] + "_1")

                msg = "GMP " + cmdArgs[1] + "_2"
                sock.sendto(msg.encode('utf-8') , (cmdArgs[3] , self.port))
                ACK , addr = sock.recvfrom(100)
                data = ACK.decode('utf-8')
                yPart = self.fSender.reciveFile(cmdArgs[1] + "_2")

                msg = "GMP " + cmdArgs[1] + "_3"
                sock.sendto(msg.encode('utf-8') , (cmdArgs[4] , self.port))
                ACK , addr = sock.recvfrom(100)
                data = ACK.decode('utf-8')
                zPart = self.fSender.reciveFile(cmdArgs[1] + "_3")

                fileInBytes = xPart + yPart + zPart
                self.fSender.writeFileOnSystem(fileInBytes,cmdArgs[1])

                msg = "RF 1 " + cmdArgs[1]
                sock.sendto(msg.encode('utf-8') , addr)
                ACK , addr = sock.recv(100)
                data = ACK.decode('utf-8')
                if(data[0] == "RTR"):
                    self.fSender.sendFile("./recive/" + cmdArgs[1] , addr[0])   


            elif(cmdArgs[0] == "GMP"):
                msg = "RF 1 " + cmdArgs[1]
                sock.sendto(msg.encode('utf-8') , addr)
                ACK , addr = sock.recv(100)
                data = ACK.decode('utf-8')
                if(data[0] == "RTR"):
                    self.fSender.sendFile("./recive/" + cmdArgs[1] , addr[0])   

class fileSender:

    def __init__(self , ip , port):
        self.bufferSize = 32768
        self.port = port
        self.ip = ip
        try:
            os.mkdir("./recive/")
        except OSError as e:
            print("No se pudo crear el directorio\n")

    def sendFile(self , path , ip):
        f = open(path , "rb")
        fileInBytes = f.read()
        fileSize = f.tell()

        sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        sock.bind((self.ip , self.port))
        print("IP TO CONECT: %s" % ip)
        sock.connect((ip , self.port))
        x = 0
        while (self.bufferSize * x < fileSize):
            block = fileInBytes[self.bufferSize * x : self.bufferSize * x + self.bufferSize - 1]
            sock.sendall(block)
            ack = sock.recv(self.bufferSize)
        print("Envio completo")

    def reciveFile(self , name):
        sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        sock.bind((self.ip, self.port -1))
    #    sock.settimeout(5.0)
        sock.listen()
        conn , addr = sock.accept()
        print("Coneccion establecida")
        fileInBytes = b''
        with conn:
            print("Recebiendo archivo")
            while True:
                try:
                    query = sock.recv(self.bufferSize)
                except socket.timeout as tOut:
                    break
                
                if not query:
                    break
                fileInBytes += query
                sock.sendall(b'ACK')
        print("Archivo recibido")
        return fileInBytes
    
    def writeFileOnSystem(self, fileInBytes , name):
        f = open("./recive/" + name , "wb+")
        f.write(fileInBytes)
        f.close()




fsend = fileSender("192.168.0.4",34523)


while True:
    try:
        inp = input().split()
        print(inp)
        if(inp[0] == "SEND"):
            fsend.sendFile(inp[1] , inp[2])
        else:
            fsend.reciveFile(inp[1])
    except KeyboardInterrupt as ex:
        break

    
