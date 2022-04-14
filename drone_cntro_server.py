import socket
import sys
# 參數
SOCKET_IP = "192.168.0.2" 
SOCKET_PORT = 5000
CMD_DESCIBTIONS = {"W":"(W) forward", "S":"(S) backward", "A":"(A) pan left", "D":"(D) pan right", "I": "(I)flight higher", "K":"(K)flight lower", "J":"(J)turn left", "L":"turn fight", "P": "(P)take off/landing"}
COMMAND_LIST =["W","S", "A", "D", "I", "J", "K", "L", "P"]#前後左右

# -------------------
skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
skt.bind((SOCKET_IP, SOCKET_PORT));
skt.listen(5)

print('server start at: %s:%s' % (SOCKET_IP, SOCKET_PORT))
print('wait for connection...')


while True:
    conn, addr = skt.accept()
    print('connected by ' + str(addr))
    print('#######################')
    for key in CMD_DESCIBTIONS:
        print("###  "+CMD_DESCIBTIONS[key])
    print('#######################')
    while True:
        input_str = input().upper()
        if "P" == input_str:
            conn.sendall("P".encode("utf-8"))
            break;
        for in_char in input_str:
            for cmd in COMMAND_LIST:
                if cmd == in_char:
                    try:
                        cmd = cmd + "\n"
                        conn.sendall(cmd.encode("utf-8"))
                        print("Message send successfully")
                    except socket.error: 
                        print(socket.error.errno)
                        print('error sending')
            
    print('conn close!')
    conn.close()