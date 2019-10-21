import sys
import os
import time
import threading
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from Server import FileTransfer

class Whatcher:
    def __init__(self):
        self.event_handler = FileSystemEventHandler()
        self.event_handler.on_created = self.on_created
        self.event_handler.on_deleted = self.on_deleted
        self.event_handler.on_modified = self.on_modified
        self.event_handler.on_moved = self.on_moved
        self.my_observer = Observer()

        self.fileT = FileTransfer()

        self.path = self.fileT.gs.dir


    def on_created(self, event):
        if(event.is_directory):
            print(f"Folder, {event.src_path} creado!")
            MSG = "mkdir " + event.src_path[14:] + "/"
            print(MSG)
            self.callServers(MSG)
            
            #Send message to create folder

    def on_deleted(self, event):
        print(f"Se elimino {event.src_path}!")
        MSG = "delete " + event.src_path[14:] + "/ " + str(event.is_directory)
        print(MSG)
        self.callServers(MSG)
        #send message to delete file or folder

    def on_modified(self, event):
        if(event.src_path != "."):
            if not event.is_directory:
                print(f"Se a Agregado/Modificado, {event.src_path}")
                MSG = "upload " + os.path.basename(event.src_path) + " " + os.path.dirname(event.src_path)[14:] + "/ " + str(os.stat(event.src_path).st_size)
                print(MSG)
                for X in self.fileT.listOfServers:
                    th = threading.Thread(target=self.fileT.sendFile , args=(event.src_path, MSG , X,))
                    th.setDaemon(True)
                    th.start()

        #send message to upload file

    def on_moved(self, event):
        print(f"Se movio {event.src_path} a {event.dest_path}")
        MSG = "move " + event.src_path + " " + event.dest_path
        print(MSG)
        self.callServers(MSG)

    def callServers(self , MSG):
        for X in self.fileT.listOfServers:
                self.fileT.sendMessage(X,MSG)

    def startWhatch(self):
        go_recursively = True
        self.my_observer.schedule(self.event_handler, self.path, recursive=go_recursively)
        self.my_observer.start()
    
    def __del__(self):
        self.my_observer.stop()
        self.my_observer.join()
        self.fileT.destroy()

    def destroy(self):
        self.my_observer.stop()
        self.my_observer.join()
        self.fileT.destroy()
        
    

wt = Whatcher()
time.sleep(10)
wt.startWhatch()
active = True
while active:
    x = input().split()
    if(x[0] == "exit" or x[0] == "0"):
        active = False
    elif(x[0] == "add"):
        wt.fileT.addServer(x[1])
wt.destroy()
