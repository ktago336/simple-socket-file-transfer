import os
import hashlib
import pickle
import socket
import time
import shutil

class sync:

    

    def __init__(self):
        pass


    def checkPath(self):
        if not os.path.isfile('path.cfg'):
            self.path=self.setPath()
            print('current path WASNT existed and is {}'.format(self.path))
            

        else:
            with open('path.cfg','rb') as inp:
                self.path = pickle.load(inp)
            print('current path exists and is {}'.format(self.path))
            inp.close()

    def getWorkingPath(self):
        self.workingPath=(self.path+'/files')
        return self.workingPath

    def getPath(self):
        return self.path
            
    def setPath(self):
        print('no path.cfg file detected. Enter working path, or leave to set current direcory\n')
        path=input().replace('\\','/')
        if (path):
            with open('path.cfg','wb') as out:
                pickle.dump(path,out)
                out.close()
            return path
            
        else:
            path=os.getcwd().replace('\\','/')
            with open('path.cfg','wb') as out:
                pickle.dump(path,out)
                out.close()
            return path
    
    def updateFile(self,filePath, path_to_create):
        mode=None
        port=9090
        ##socket menu
        while True:
            mode=input('listening mode? y/n\n')
            if mode=='y':
                break
            elif mode=='n':
                break

        ##RECV mode
        if mode=='y':
        
            sock = socket.socket()
            
            iphost = input('enter ip to bind or press enter for 0.0.0.0\n')
            port = 9090
            sock.bind((iphost, port))
            print('listening...', sock.getsockname())
            

            while True:
                sock.listen(10)        
                conn, addr = sock.accept()
                print('CONNECTED')
                print('connected to:', addr)
                
                dir = (conn.recv(1024)).decode ('UTF-8')
                print (self.getWorkingPath()+'recieved {}  dir'.format(dir))
                try:
                    os.makedirs(self.getWorkingPath()+dir)
                except FileExistsError:
                    pass
                name_f = (conn.recv(1024)).decode ('UTF-8')
                print ('recieved {}  NAME'.format(name_f))
                f = open(self.getWorkingPath()+r'{}'.format(name_f),'wb')

                while True:
                    l = conn.recv(1024)
                    f.write(l)
                    if not l:
                        break
                f.close()
                print ('sucseed')
                print('File {} received'.format(name_f))
                time.sleep(1)
                conn.close()
            conn.close()
            sock.close()

        ##SEND mode
        elif mode=='n':
            if not os.path.isfile('addr.cfg'):
                addr = open('addr.cfg', 'w')
                addr.write(input('enter destination ip\n'))
                addr.close()
            while True:
                yorn=input('rewrite destination ip?\n')
                if yorn=='y':
                    addr = open('addr.cfg', 'w')
                    addr.write(input('enter destination ip\n'))
                    addr.close()
                    break
                elif yorn=='n':
                    break
            addr = open('addr.cfg', 'r')
            ip=addr.read()
            addr.close()
            
            print ('send mode')
            sock=socket.socket()
            sock.connect((ip, port))
          
            sock.send((bytes(path_to_create,encoding='UTF-8')))
            
            time.sleep(0.1)
            pathToSend='/' + filePath[len(os.getcwd())+1:].replace('\\','/')           
            sock.send((bytes(pathToSend,encoding='UTF-8')))
            
            print(pathToSend)#####
            time.sleep(0.1)
            f=open(filePath,  "rb")
            l=f.read(1024)
            while (l):
                sock.sendall(l)
                l=f.read(1024)
            sock.close()
            f.close()
            time.sleep(0.1)
            print ('{} sucseed'.format(filePath[len(os.getcwd()):]))

    def checkSum(self,path):
        dictFiles = {}
        with open('data.cfg','rb') as inp:
            dictFiles = pickle.load(inp)
        for root, dirs, files in os.walk(path):
            for file in files:
                with open (os.path.join(root,file),'rb') as current:
                    h=hashlib.md5(bytes(current.read(8192)))
                    while True:
                        data=bytes(current.read(8192))
                        if not data:
                            break
                        h.update(data)

                    try:    
                        if dictFiles[os.path.join(root,file)]!=h.hexdigest():
                            print('{} CHANGED. UPDATING...'.format(file))
                            print(root[len(os.getcwd()):])
                            self.updateFile(os.path.join(root,file),root[len(os.getcwd()):].replace('\\','/'))
                            dictFiles[os.path.join(root,file)]=h.hexdigest()
                        else:
                            print('{} OK'.format(file))
                    except KeyError:
                        dictFiles[os.path.join(root,file)]=h.hexdigest()
                        print('{} NEW FILE. UPDATING...'.format(file))
                        self.updateFile(os.path.join(root,file))
                    
                current.close()
        with open('data.cfg','wb') as out:
            pickle.dump(dictFiles,out)
        out.close()
        print(dictFiles)
        
    def createCfg(self, path):
        listOfFiles=[]
        dictFiles={}
        for root, dirs, files in os.walk(str(path)):
            for file in files:
                with open (os.path.join(root,file),'rb') as current:
                    h=hashlib.md5(bytes(current.read(8192)))
                    while True:
                        data=bytes(current.read(8192))
                        if not data:
                            dictFiles[os.path.join(root,file)]=h.hexdigest()
                            print(h.hexdigest())

                            print(os.path.join(root,file)[len(os.getcwd()):])
                            
                            break
                        h.update(data)
                current.close()
        dictSums=dict.fromkeys(listOfFiles)
        with open('data.cfg','wb') as out:
            pickle.dump(dictFiles,out)
        out.close()

    def firstRun(self, path):
        createCfg(path)
        print('setting up files folder...')
        if not os.path.exists(path+'/files'):
            os.mkdir(path+'/files') 
        print('checking cfg...')
        if not os.path.isfile(path+'/addr.cfg'):
                addr = open(path+'addr.cfg', 'w')
                addr.write(input('enter destination ip\n'))
                addr.close()
        checkSum(path+'/files')
    
s=sync()

s.checkPath()
#os.mkdir(s.getWorkingPath()+'/dir1')
print('\n\npaths\n\n')
print(s.getWorkingPath())
print(s.getPath())
print('\n\n')
#s.createCfg(s.getWorkingPath())
s.checkSum(s.getWorkingPath())

    ####


    #name_f = ('./files/beb2.txt')
    #f = open(name_f,'wt')
    #f.write('aaaaasadfsdfds')
    #f.close()
    #print ('sucseed')
    #print('File {} received'.format(name_f))
    ####

    #createCfg(path)
    #updateFile(path)
#print(os.getcwd())
    #checkSum(path)


