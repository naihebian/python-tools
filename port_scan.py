from threading import Thread, activeCount
import socket
import os
import sys
def test_port(ip,port):
    os.system('title '+'[*]The scan port open'+str(port))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:

        indicator = s.connect_ex((ip, port))
        if indicator == 0:
            print 'The Open port',port
        s.close()
    except:
        pass

if __name__=='__main__':
    try:
        ip = sys.argv[1]
    except:
        print '[-] Please enter the destination IP!'
        exit()
    i = 0
    while i < 65536:
        if activeCount() <= 200:
            Thread(target = test_port, args = (ip, i)).start()
            i = i + 1
    while True:
        if activeCount() == 2:
            break
