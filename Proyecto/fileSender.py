import os
import socket

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
#        sock.bind((self.ip , self.port))
        print("IP TO CONECT: %s" % ip)
        sock.connect((ip , self.port))
        x = 0
        while (self.bufferSize * x < fileSize):
            block = fileInBytes[self.bufferSize * x : self.bufferSize * x + self.bufferSize - 1]
            sock.sendall(block)
            ack = sock.recv(self.bufferSize)
            x += 1
            print("PK1")
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
            block = fileInBytes[self.bufferSize * x : self.bufferSize * x + self.bufferSize - 1]
            sock.sendall(block)
            ack = sock.recv(self.bufferSize)
            x += 1
            print("PK1")
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
        with conn:
            print("Recebiendo archivo")
            while True:
                try:
                    query = conn.recv(self.bufferSize)
                except conn.timeout as tOut:
                    break
                print("Recive")
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
