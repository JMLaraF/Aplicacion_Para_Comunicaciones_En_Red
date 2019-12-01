import os
import socket
from time import sleep
from fileSender import *


class Server:
    def __init__(self):
        self.ip = "10.114.45."
        self.port = 34567
        self.fSender = fileSender(self.ip , self.port-1)
    #    self.listOfServers = ["10.114.45.181","10.114.45.210","10.114.45.23"]


    def listener(self):
        sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
        sock.bind((self.ip , self.port))
        print("Is listening")
        while True:
            try:
                data , addr = sock.recvfrom(100)
                cmdArgs = data.decode('utf-8').split()
                print(cmdArgs[0])
            except KeyboardInterrupt as ex:
                break
            if(cmdArgs[0] == "RF"):
                fileInBytes = self.fSender.reciveFile(sock,addr)
                if(cmdArgs[1] == '0'):
                    leftSize = len(fileInBytes) // 3
                    rigthSize = 2*len(fileInBytes) // 3
                    xPart = fileInBytes[0:leftSize]
                    yPart = fileInBytes[leftSize:rigthSize]
                    zPart = fileInBytes[rigthSize:len(fileInBytes)]
                    sock.sendto(("RF 1 " + cmdArgs[2] + "_1").encode('utf-8'),(cmdArgs[3] , self.port))
                    ACK = sock.recvfrom(100)
                    self.fSender.sendFileB(xPart,cmdArgs[3])
                    sock.sendto(("RF 1 " + cmdArgs[2] + "_2").encode('utf-8'),(cmdArgs[4] , self.port))
                    ACK = sock.recvfrom(100)
                    self.fSender.sendFileB(yPart,cmdArgs[4])
                    sock.sendto(("RF 1 " + cmdArgs[2] + "_3").encode('utf-8'),(cmdArgs[5] , self.port))
                    ACK = sock.recvfrom(100)
                    self.fSender.sendFileB(zPart,cmdArgs[5])
                else:
                    self.fSender.writeFileOnSystem(fileInBytes , cmdArgs[2])
            elif(cmdArgs[0] == "GMF"):
                hostIP = addr[0]
                msg = "GMP " + cmdArgs[1] + "_1"
                sock.sendto(msg.encode('utf-8') , (cmdArgs[2] , self.port))
                ACK , addr = sock.recvfrom(100)
                data = ACK.decode('utf-8')
                xPart = self.fSender.reciveFile(sock , addr)

                msg = "GMP " + cmdArgs[1] + "_2"
                sock.sendto(msg.encode('utf-8') , (cmdArgs[3] , self.port))
                ACK , addr = sock.recvfrom(100)
                data = ACK.decode('utf-8')
                yPart = self.fSender.reciveFile(sock , addr)

                msg = "GMP " + cmdArgs[1] + "_3"
                sock.sendto(msg.encode('utf-8') , (cmdArgs[4] , self.port))
                ACK , addr = sock.recvfrom(100)
                data = ACK.decode('utf-8')
                zPart = self.fSender.reciveFile(sock , addr)

                fileInBytes = xPart + yPart + zPart
            #    self.fSender.writeFileOnSystem(fileInBytes,cmdArgs[1])

                msg = "RF 1 " + cmdArgs[1]
                sock.sendto(msg.encode('utf-8') , (hostIP , 34587))
                ACK , addr = sock.recvfrom(100)
                data = ACK.decode('utf-8')
                if(data == "RTR"):
                    print("Sending last part")
                    self.fSender.sendFileB(fileInBytes , hostIP)   


            elif(cmdArgs[0] == "GMP"):
                msg = "RF 1 " + cmdArgs[1]
                sock.sendto(msg.encode('utf-8') , addr)
                ACK , addr = sock.recvfrom(100)
                data = ACK.decode('utf-8')
                if(data == "RTR"):
                    self.fSender.sendFile("./recive/" + cmdArgs[1] , addr[0])   


# ip = "192.168.0.4"
serv = Server()
serv.listener()

# s = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
# s.bind((ip,34587))

# fsend = fileSender(ip,34566)


# while True:
#     try:
#         inp = input().split()
#         print(inp)
#         if(inp[0] == "send"):
#             msg = "RF 0 " + inp[1] + " 10.114.45.181 10.114.45.210 10.114.45.23"
#             print(msg)
#             s.sendto(msg.encode('utf-8') ,(inp[3] , 34567))
#         #    sleep(2.0)
#             ACK = s.recvfrom(100)
#             fsend.sendFile(inp[2],inp[3])
#         else:
#             msg = "GMF " + inp[1] + " 10.114.45.181 10.114.45.210 10.114.45.23"
#             print(msg)
#             s.sendto(msg.encode('utf-8') ,(inp[2] , 34567))
#         #    fileX = fsend.reciveFile(s,)
#         #    fsend.writeFileOnSystem(fileX,inp[1])
#     except KeyboardInterrupt as ex:
#         break

    
