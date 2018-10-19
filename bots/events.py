import socket, sys

HOST = ''
PORT = 8063

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('socket created')

try:
    s.bind( (HOST, PORT) )
except socket.error as msg:
    print('bind failed: ' + str(msg[0]) + ' ' + msg[1])
    sys.exit(1)

print('socket bind complete')

s.listen(10)
print('socket now listening')

def clientthread(conn):
    conn.send(b'hys\n')

    while True:
        data = conn.recv(1024)
        reply = b'OK...' + data
        if not data:
            break

        conn.sendall(reply)

    conn.close()

while 1:
    conn, addr = s.accept()
    print('connected with ' + addr[0] + ':' + str(addr[1]))
    clientthread(conn)
s.close()
