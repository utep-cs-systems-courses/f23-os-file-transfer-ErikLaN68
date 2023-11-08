#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os, time
sys.path.append("../lib")       # for params
import params
import mytar

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

pidAddr = {}

if paramMap['usage']:
    params.usage()

# server code to be run by child
def chatWithClient(connAddr):
    # Can't unpack the socket object 
    # sock, addr = connAddr
    print(f'Child: pid={os.getpid()} connected to client at {addr}')
    # print('Connected by', addr)
    framedNameAndContents = mytar.framer(["foo.txt","goo.gif"])
    connAddr.send(framedNameAndContents)
    connAddr.shutdown(socket.SHUT_WR)
    sys.exit(0)                 # terminate child

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.settimeout(5)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

while True:
    # reap zombie children
    while pidAddr.keys():
        # check for zombies. If none don't hang
        if (waitResult := os.waitid(os.P_ALL, 0, os.WNOHANG | os.WEXITED)):
            zPid, zStatus = waitResult.si_pid, waitResult.si_status
            print(f"""zombie reaped:
            \tpid={zPid}, status={zStatus}
            \twas connected to {pidAddr[zPid]}""")
            del pidAddr[zPid]
        else:
            break #No zombies break
    print(f"Currently {len(pidAddr.keys())} clients")
    
    try:
        conn, addr = s.accept() # wait until incoming connection request (and accept it)
    except TimeoutError:
        conn = None
    
    if conn is None:
        continue
    
    print(conn)
    forkResult = os.fork()
    if forkResult == 0:
        s.close()
        chatWithClient(conn)
    
    #parent
    print(conn)
    # can't unpack conn which is socket object
    addr = conn
    conn.close()
    pidAddr[forkResult] = addr