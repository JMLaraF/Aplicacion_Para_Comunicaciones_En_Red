import os
import time
import shutil

class Gestor:                               #Gestor del repositorio
    def __init__(self, repo_Size):
        self.dir = "./REPOSITORIO/"         #Direccion del repositorio principal
        self.actual_Size = 0                #Tamaño actual del repositorio
        self.max_Size = repo_Size           #Tamaño maximo que puede tener este
        try:                                
            os.mkdir(self.dir)              #Trata de crear la carpeta del repositorio, si ya exite sale con codigo de error -2
        except OSError as e:
            print("No se pudo crear el directorio\n")
            exit(-2)

    def __init__(self):
        self.dir = "./REPOSITORIO/"
        self.actual_Size = 0
        self.max_Size = 1073741824
        try:
            os.mkdir(self.dir)
        except OSError as e:
            print("No se pudo crear el directorio\n")
            exit(-2)

    def removeRepository(self , path):
        for r, d, f in os.walk(path):
            for file in f:
                os.remove(os.path.join(r, file))
            for folders in d:
                os.rmdir(os.path.join(r, folders))


    def UploadFile(self, rutaArchivo , rutaDestino):
        fileSize = os.stat(rutaArchivo).st_size
        if(self.max_Size < self.actual_Size + fileSize):
            return -1
        if(os.path.isdir(self.dir + rutaDestino) == False):
            self.makeFolder(rutaDestino)
        if(os.path.isfile(self.dir + rutaDestino + os.path.basename(rutaArchivo))):
            option = 0#input()
            if(option != "0"):
                return -3
        try:
            shutil.copyfile(rutaArchivo, self.dir + rutaDestino + os.path.basename(rutaArchivo))
        except IOError as e:
            return -3
        return 0
    def makeFolder(self , rutaDestino):
        try:
            os.makedirs(self.dir + rutaDestino)
        except OSError as e:
            return -2

    def RemoveFolder(self , path):
        print(self.dir + path)
        if not (os.path.isdir(self.dir + path)):
            return -5
        if (os.listdir(self.dir + path)):
            print("Deseas remover todos los archivos y subcarpetas")
            option = 0#input()
            if(option != "0"):
                return -6
            try:
                shutil.rmtree(self.dir + path)
            except IOError as e:
                return -5
        else:
            try:
                os.rmdir(self.dir + path)
            except OSError as e:
                return -5
        return 0

    def RemoveFile(self , path):
        print(self.dir + path)
        if not (os.path.isfile(self.dir + path)):
            return -4
        try:
            os.remove(self.dir + path)
        except OSError as e:
            return -4
        return 0

    def move(self , src_path , dest_path):
        try:
            shutil.move(self.dir + src_path,self.dir + dest_path)
        except FileNotFoundError as e:
            return -1
        return 0
    def listFolders(self , path):
        #print(self.dir + path)
        elements = os.listdir(self.dir + path)
        Folders = [f for f in elements if os.path.isdir(self.dir + path + f)]
        return Folders
    def listFiles(self , path):
        #print(self.dir + path)
        elements = os.listdir(self.dir + path)
        #print(elements)
        Files = [f for f in elements if os.path.isfile(self.dir + path + f)]
        return Files

    def __del__(self):
        try:
            shutil.rmtree(self.dir)
        except FileNotFoundError as e:
            pass

    def destroy(self):
        try:
            shutil.rmtree(self.dir)
        except FileNotFoundError as e:
            pass

# gestor = Gestor()
# comando = input()
# while(comando != "exit"):
#     cmdArgs = comando.split()
#     if(cmdArgs[0] == "upload"):
#         if(len(cmdArgs) == 3):
#             result = gestor.UploadFile(cmdArgs[1] , cmdArgs[2])
#             print("upload => %d" % result)
#     elif(cmdArgs[0] == "rmfile"):
#         if(len(cmdArgs) == 2):
#             result = gestor.RemoveFile(cmdArgs[1])
#             print("remove file => %d" % result)
#     elif(cmdArgs[0] == "rmfolder"):
#         if(len(cmdArgs) == 2):
#             result = gestor.RemoveFolder(cmdArgs[1])
#             print("remove folder => %d" % result)
#     elif(cmdArgs[0] == "move"):
#         if(len(cmdArgs) == 3):
#             result = gestor.move(cmdArgs[1],cmdArgs[2])
#             print(result)
#     comando = input()
# print("SALIO")