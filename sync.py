import sys
import socket
import time
import os
import setupsync as start
path=os.getcwd()+'/files'
Port=9090
try:
    
    args=sys.argv[1]
    if args=='s':   
        start.firstRun()
except IndexError:
    pass
s=sync()
s.updateFile('','')
start.createCfg()
start.checkSum()
start.updateFile('./files/beb1.txt')

sync.checkPath()

#if recieving
if sendOrRecv=='0':
    print('reading mode on')
    sock=socket.socket()
    sock.bind(('', Port))
    print('listening...')
    sock.listen(1)
    conn, addr=sock.accept()

    print('Connection established ', addr)

    f=open(dataToSend,'w')
    f.close()
    f=open(dataToSend,'a')
    while True:
        data=conn.recv(2048)
        if not data:
            break
        f.write(data)
    conn.close()
    f.close()
    print('OK')
if sendOrRecv=='s':
    print ('send mode')
    sock=socket.socket()
    sock.connect((ip, port))

    f_name=input('data to send\n')
    sock.send((bytes(f_name,encoding='UTF-8')))
    time.sleep(0.1)
    f=open(f_name,  "rb")
    l=f.read(1024)
    while (l):
        sock.sendall(l)
        l=f.read(1024)
    sock.close()
    f.close()
    print ('sucseed')
    
if sendOrRecv=='r':
    
    sock = socket.socket()
    ip = "10.0.0.24"
    port = 22
    sock.bind((ip, port))
    print('listening...', sock.getsockname())
    sock.listen(10)
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
        conn.close()
    print ('sucseed')
    print('File received')

    sock.close()
    
