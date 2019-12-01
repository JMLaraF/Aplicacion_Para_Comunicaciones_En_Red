import os
import socket

class fileSender:

    def __init__(self , ip , port):
        self.bufferSize = 4194304
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
#        sock.bind((self.ip , self.port))
        print("IP TO CONECT: %s" % ip)
        sock.connect((ip , self.port))
        x = 0
        while (self.bufferSize * x < fileSize):
            block = fileInBytes[self.bufferSize * x : self.bufferSize * (x+1)]
            sock.sendall(block)
            ack = sock.recv(self.bufferSize)
            x += 1
            if(x%5 == 0):
                print("Enviando...")
        print("Envio completo")
    #    sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        

    def sendFileB(self , fileInBytes , ip):

        fileSize = len(fileInBytes)

        sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    #    sock.bind((self.ip , self.port))
        print("IP TO CONECT: %s" % ip)
        sock.connect((ip , self.port))
        x = 0
        while (self.bufferSize * x < fileSize):
            block = fileInBytes[self.bufferSize * x : self.bufferSize * (x+1)]
            sock.sendall(block)
            ack = sock.recv(self.bufferSize)
            x += 1
            if(x%5 == 0):
                print("Enviando...")
    #        print("PK1")
        print("Envio completo")
    #    sock.shutdown(socket.SHUT_RDWR)
        sock.close()

    def reciveFile(self , sockUDP , addrUDP):
        sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        sock.bind((self.ip, self.port))
    #    sock.settimeout(5.0)
        sock.listen()
        sockUDP.sendto(b'RTR' , addrUDP)
        conn , addr = sock.accept()
        print("Coneccion establecida")
        fileInBytes = b''
        x = 0
        with conn:
            print("Recebiendo archivo")
            while True:
                x += 1
                try:
                    query = conn.recv(self.bufferSize)
                except conn.timeout as tOut:
                    break
                if(x%5 == 0):
                    print("Recibiendo...")
                if not query:
                    break
                fileInBytes += query
                conn.sendall(b'ACK')
        print("Archivo recibido")
    #    sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        return fileInBytes
    
    def writeFileOnSystem(self, fileInBytes , name):
        f = open("./recive/" + name , "wb+")
        f.write(fileInBytes)
        f.close()
