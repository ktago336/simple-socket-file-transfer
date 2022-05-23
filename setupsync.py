import os
from sys import platform
import hashlib
import pickle

def updateFile(filePath):
    pass


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
    return False


path=os.getcwd()+'/files'

checkSum(path)


