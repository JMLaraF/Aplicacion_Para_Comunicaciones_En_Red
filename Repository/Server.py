import socket
import os
import shutil
import threading
import gc
from Gestor import Gestor

#Code copided from stackOverflow Brian R. Bondy
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")
#####################


class FileTransfer:
    listOfServers = []

    def __init__(self , ip , port):
        self.ip = ip
        self.port = port
        self.dir = "./RECIVE/"
        self.makeReciveFolder()
        self.gs = Gestor()
        self.buffSize = 32768
        self.active = True

    def __init__(self):
        self.ip = "192.168.0.9"
        print(self.ip)
        self.port = 5050
        self.dir = "./RECIVE/"
        self.makeReciveFolder()
        self.gs = Gestor()
        self.buffSize = 32768
        self.active = True
        th = threading.Thread(target=self.waitPetitions , args=())
        th.setDaemon(True)
        th.start()


    def addServer(self, ip):
        self.listOfServers.append(ip)

    def makeReciveFolder(self):
        if(os.path.isdir(self.dir) == False):
            try:
                os.makedirs(self.dir)
            except OSError as e:
                print(e)        
                exit -1

    def checkConetion(self , tcp_sock , port):
        try:
            tcp_sock.bind((self.ip , port))
            return True
        except OSError as e:
            return False

    def sendMessage(self, ip , MSG):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(MSG.encode('utf-8') , (ip,self.port))

    def waitPetitions(self):
        sock =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.ip,self.port))
        while self.active:
            data , addr = sock.recvfrom(1024)
            cmdArgs = data.decode('utf-8').split()
            print(cmdArgs)
            if(cmdArgs[0] == "delete"):
                self.deleteQuery(cmdArgs[1] , str2bool(cmdArgs[2]))
            elif(cmdArgs[0] == "mkdir"):
                self.makeDirQuery(cmdArgs[1])
            elif(cmdArgs[0] == "move"):
                self.moveQuery(cmdArgs[1] , cmdArgs[2])
            elif(cmdArgs[0] == "upload"):
                if(len(cmdArgs) == 4):
                    threadFile = threading.Thread(target=self.ReciveFile , args=(cmdArgs[1] , cmdArgs[2] , int(cmdArgs[3]) , addr))
                    threadFile.setDaemon(True)
                    threadFile.start()
                elif(len(cmdArgs) == 3):
                    threadFile = threading.Thread(target=self.ReciveFile , args=(cmdArgs[1] , "" , int(cmdArgs[3]) , addr))
                    threadFile.setDaemon(True)
                    threadFile.start()

    #         if(cmdArgs[0] == "list"):
    #             folders = self.gs.listFolders(cmdArgs[1][1:])
    #             files = self.gs.listFiles(cmdArgs[1][1:])
    #             MSG = ""
    #             for i in folders:
    #                 MSG += "folder => " + str(i) + "\n"
    #             for i in files:
    #                 MSG += "files => " + str(i) + "\n"
    #             print(MSG)
    #             sock.sendto(MSG.encode('utf-8') , (addr))

    #         if(cmdArgs[0] == "download"):
    #             if(os.path.isfile(self.gs.dir + cmdArgs[1])):
    #                 udp_sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
    #                 port = self.port + 1
    #                 while (self.checkConetion(udp_sock , port) == False):
    #                     port += 1
    #                 MSG = "ACK " + str(port)
    #                 threadFile = threading.Thread(target=self.sendFile , args=(udp_sock , cmdArgs[1][1:], sock , MSG , addr))
    #                 threadFile.setDaemon(True)
    #                 threadFile.start()
    #             else:
    #                 MSG = "NFF"
    #                 sock.sendto(MSG.encode('utf-8') , (addr))

    def deleteQuery(self, path , is_folder):
        if is_folder:
            self.gs.removeRepository(path)
        else:
            self.gs.RemoveFile(path)
    def moveQuery(self, src , dest):
        self.gs.move(src,dest)
    
    def makeDirQuery(self , path):
        self.gs.makeFolder(path)

    def sendFile(self , filePath , MSG , ip):
        print("Inicio")
        f = open(filePath , "rb")
        FileInBytes = f.read()
        fileSize = f.tell()
        self.buffSize = 32768

        ftotal = fileSize
        steps = 0

        udp_sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
        port = self.port + 1
        while (self.checkConetion(udp_sock , port) == False):
            port += 1

        udp_sock.sendto(MSG.encode('utf-8'),(ip,self.port))
        ACK , addr = udp_sock.recvfrom(1024)

        i = 0
        while(fileSize > 0):
            block = FileInBytes[i:i+self.buffSize]
            udp_sock.sendto(block,addr)
            i += self.buffSize
            fileSize -= self.buffSize
            flag , xxx = udp_sock.recvfrom(3)
            steps += 1
            if(steps >= 200):
                print(" %c %d Completo." % ( '%' , 100-(fileSize*100/ftotal)))
                steps = 0
        udp_sock.sendto(b'',addr)
        print("Llego %s" % filePath)
        f.close()

    def ReciveFile(self , fileName , filePath , fileSize , addr):
        
        udp_sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
        port = self.port + 1
        while (self.checkConetion(udp_sock , port) == False):
            port += 1
        MSG = "UCF " + self.ip + " " + str(port)
        udp_sock.sendto(MSG.encode('utf-8') , (addr))
        
        print("Inicio")
        newFile = b""
        
        ftotal = fileSize
        steps = 0
        while(fileSize > 0):
            query , XXX = udp_sock.recvfrom(self.buffSize)
            newFile += query
            fileSize -= self.buffSize
            udp_sock.sendto(b'START' , addr)
            steps += 1
            if(steps >= 200):
                print(" %c %d Completo." % ( '%' , 100-(fileSize*100/ftotal)))
                steps = 0

        udp_sock.sendto(b'START' , addr)
        print("Llego %s" % fileName)
        udp_sock.close()

        f = open(self.dir + fileName, "wb+")
        f.write(newFile)
        f.close()
        self.gs.UploadFile(self.dir + fileName , filePath)
        
    def __del__(self):
        try:
            shutil.rmtree(self.dir)
            self.gs.destroy()
        except FileNotFoundError as ex:
            pass

    def destroy(self):
        try:
            shutil.rmtree(self.dir)
            self.gs.destroy()
        except FileNotFoundError as ex:
            pass


# f = FileTransfer()
# TH = threading.Thread(target=f.waitPetitions , args=())
# TH.setDaemon(True)
# TH.start()
# while f.active:
#     x = input().split()
#     if(x[0] == "exit" or x[0] == "0"):
#         f.active = False
#     elif(x[0] == "add"):
#         f.addServer(x[1])

# f.destroy()
