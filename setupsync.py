import os
import hashlib
import pickle
import socket

def updateFile(filePath):
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
        return
        sock.listen(1)
        print('CONNECTED')

        while True:
            conn, addr = sock.accept()
            print('connected to:', addr)
            
            name_f = (conn.recv(1024)).decode ('UTF-8')
            f = open(name_f,'wb')

            while True:
                l = conn.recv(1024)
                f.write(l)
                if not l:
                    break
            f.close()
            print ('sucseed')
            print('File {} received'.format(f_name))
            conn.close()
            break
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

        sock.send((bytes(filePath[len(os.getcwd())+1:],encoding='UTF-8')))
        time.sleep(0.1)
        f=open(filePath,  "rb")
        l=f.read(1024)
        while (l):
            sock.sendall(l)
            l=f.read(1024)
        sock.close()
        f.close()
        print ('{} sucseed'.format(filePath[len(os.getcwd()):]))

def checkSum(path):
    dictFiles = {}
    with open('data.cfg','rb') as inp:
        dictFiles = pickle.load(inp)
    print(dictFiles)
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
                        updateFile(os.path.join(root,file))
                        dictFiles[os.path.join(root,file)]=h.hexdigest()
                    else:
                        print('{} good'.format(file))
                except KeyError:
                    dictFiles[os.path.join(root,file)]=h.hexdigest()
                    updateFile(os.path.join(root,file))
                
            current.close()
    with open('data.cfg','wb') as out:
        pickle.dump(dictFiles,out)
    print(dictFiles)
    
def createCfg(path):
    listOfFiles=[]
    dictFiles={}
    for root, dirs, files in os.walk(path):
        for file in files:
            with open (os.path.join(root,file),'rb') as current:
                h=hashlib.md5(bytes(current.read(8192)))
                while True:
                    data=bytes(current.read(8192))
                    if not data:
                        dictFiles[os.path.join(root,file)]=h.hexdigest()
                        print(h.hexdigest())
                        break
                    h.update(data)
            current.close()
    dictSums=dict.fromkeys(listOfFiles)
    with open('data.cfg','wb') as out:
        pickle.dump(dictFiles,out)
    print(dictFiles)

def firstRun():
    path=os.getcwd()
    
    

   
    print('setting up files folder')
    os.mkdir("files")
    checkSum(os.getcwd()+'/files')


path=os.getcwd()+'/files'
createCfg(path)
updateFile(path)
print(os.getcwd())
checkSum(path)


