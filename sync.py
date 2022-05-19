import sys
import socket
import time
import os

ip=sys.argv[1]
port=5555
sendOrRecv=sys.argv[2]
    
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
    sock.bind((ip, port))
    print('listening...', sock.getsockname())
    sock.listen(10)

    while True:
        conn, addr = sock.accept()
        print('connected to:', addr)
        
        name_f = (conn.recv(1024)).decode ('UTF-8')
        f = open(name_f,'wb')

        while True:
            l = conn.recv(1024)
            f.write(l)
            print('1024 bytes writed...')
            if not l:
                print('breaking...')
                break
            
        f.close()
        conn.close()
    print ('sucseed')
    print('File received')

sock.close()
    
