import tkinter
from tkinter import filedialog
from tkinter import *
import threading
import os
from fileSender import *


class GUI:
    def __init__(self):
        self.win = tkinter.Tk()
        self.win.geometry("1200x600")
        Grid.columnconfigure(self.win , 3 , weight = 1)
        Grid.rowconfigure(self.win , 3 , weight = 1)
        

        self.label1 = Label(self.win , text ="FILES")
        self.fileLabel = Label(self.win , text = "" , borderwidth = 2 , relief = "groove" , justify = "left")
        self.saveBtn = Button(self.win , text="Enviar" , width = 10 , command = lambda: self.sendFileCmd())
        self.loadBtn = Button(self.win , text="Recibir" , width = 10 , command = lambda: self.reciveFileCmd())
        self.exploreBtn = Button(self.win , text="Examinar" , width = 10 , command = lambda: self.popupFileWindow())
        self.fileList = Listbox(self.win , borderwidth = 2 , relief = "groove")
        self.label1.grid(row = 0 , column = 0 , padx=5 , columnspan = 2)
        self.saveBtn.grid(row = 1 , column = 0 , padx=5)
        self.loadBtn.grid(row = 1 , column = 1 , padx=10)
        self.fileLabel.grid(row = 2 , column = 1 , sticky = "ew" , padx = 5 , pady = 10 , columnspan = 3)
        self.exploreBtn.grid(row = 2 , column = 0 , padx = 5)
        self.fileList.grid(row = 3 , column = 0 , columnspan = 4 , sticky = "wens")

        self.fSender = fileSender("192.168.0.4" , 34566)

        # self.serv = Server()
        # servListener = threading.Thread(target=self.serv.listener)
        # servListener.setDaemon(True)
        # servListener.start()

        self.fileToSend = ""
        self.listOfServers = ["10.114.45.152","10.114.45.181","10.114.45.210","10.114.45.23"]

        self.win.mainloop()

    def popupFileWindow(self):
        self.fileToSend = filedialog.askopenfilename(initialdir = "./",title = "Elige un archivo para mandar al servidor",filetypes = (("txt files","*.txt"),("all files","*.*")))
        self.fileLabel.config(text = self.fileToSend)

    def sendFileCmd(self):
        s = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
        s.bind((self.fSender.ip,34587))
        fName = os.path.basename(self.fileToSend)
        msg = "RF 0 " + fName
        for i in range(1,len(self.listOfServers)):
            msg += " " + self.listOfServers[i]
        print(msg)
        s.sendto(msg.encode('utf-8') ,(self.listOfServers[0] , 34567))
        #    sleep(2.0)
        ACK = s.recvfrom(100)
        
        self.fSender.sendFile(self.fileToSend,self.listOfServers[0])
        self.fileList.insert(END , fName)

    def reciveFileCmd(self):
        s = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
        s.bind((self.fSender.ip,34587))        
        fName = self.fileList.get(ACTIVE)
        msg = "GMF " + fName
        for i in range(1,len(self.listOfServers)):
            msg += " " + self.listOfServers[i]
        print(msg)
        s.sendto(msg.encode('utf-8') ,(self.listOfServers[0] , 34567))
        ACk , addr = s.recvfrom(100)
        fileInBytes = self.fSender.reciveFile(s,addr)
        self.fSender.writeFileOnSystem(fileInBytes , fName)
        #    fileX = fsend.reciveFile(s,)
        #    fsend.writeFileOnSystem(fileX,inp[1])

GUIClient = GUI()
