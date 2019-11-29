import threading
import socket
import tkinter
from tkinter import *

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

    def sendFile(self , path , ip):
        f = open(path , "rb")
        fileInBytes = f.read()
        fileSize = f.tell()

        sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        sock.bind(self.ip , self.port)
        sock.connect((ip , self.port))
        x = 0
        while (self.bufferSize * x < fileSize):
            block = fileInBytes[self.bufferSize * x : self.bufferSize * x + self.bufferSize - 1]
            sock.sendall(block)
            ack = sock.recv(self.bufferSize)
        print("Envio completo")

    def reciveFile(self , name):
        sock = socket(socket.AF_INET , socket.SOCK_STREAM)
        sock.bind(self.ip, self.port -1)
        sock.settimeout(5.0)
        sock.listenen()
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


class GUI:
    def __init__(self):
        self.win = tkinter.Tk()
        self.win.geometry("1200x600")
        Grid.columnconfigure(self.win , 3 , weight = 1)
        Grid.rowconfigure(self.win , 3 , weight = 1)
    #    Grid.columnconfigure(self.win , 3 , weight = 2)

        self.label1 = Label(self.win , text ="FILES")
        self.fileLabel = Label(self.win , text = "" , borderwidth = 2 , relief = "groove")
        self.saveBtn = Button(self.win , text="Guardar" , width = 10)
        self.loadBtn = Button(self.win , text="Cargar" , width = 10)
        self.exploreBtn = Button(self.win , text="Examinar" , width = 10)
        self.fileList = Listbox(self.win , borderwidth = 2 , relief = "groove")
        self.label1.grid(row = 0 , column = 0 , padx=5 , columnspan = 2)
        self.saveBtn.grid(row = 1 , column = 0 , padx=5)
        self.loadBtn.grid(row = 1 , column = 1 , padx=10)
        self.fileLabel.grid(row = 2 , column = 1 , sticky = "ew" , padx = 5 , pady = 10 , columnspan = 3)
        self.exploreBtn.grid(row = 2 , column = 0 , padx = 5)
        self.fileList.grid(row = 3 , column = 0 , columnspan = 4 , sticky = "wens")


        self.win.mainloop()

interfaz = GUI()

    