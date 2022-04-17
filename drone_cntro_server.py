import socket
import pygame
import time
# 參數
SOCKET_IP = "172.20.10.2" 
SOCKET_PORT = 5000
CMD_DESCIBTIONS = {"W":"(W) forward", "S":"(S) backward", "A":"(A) pan left", "D":"(D) pan right", "I": "(I)flight higher", "K":"(K)flight lower", "J":"(J)turn left", "L":"turn fight", "P": "(P)take off/landing"}
COMMAND_LIST =["W","S", "A", "D", "I", "J", "K", "L", "P"]#前後左右
pressed_char = ''
# -------------------
skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
skt.bind((SOCKET_IP, SOCKET_PORT));
skt.listen(5)

print('server start at: %s:%s' % (SOCKET_IP, SOCKET_PORT))
print('wait for connection...')


def key2Char(key):
    if key == 119:
        return 'W'
    elif key == 97:
        return 'A'
    elif key == 115:
        return 'S'
    elif key == 100:
        return 'D'
    elif key == 105:
        return 'I'
    elif key == 106:
        return 'J'
    elif key == 107:
        return 'K'
    elif key == 108:
        return 'L'
    elif key == 112:
        return 'P'
    else:
        return ''
def refrashPressedChar(pressed_char): 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pressed_char = key2Char(event.key)
        if event.type == pygame.KEYUP and key2Char(event.key) == pressed_char:
            pressed_char = ''
    return pressed_char


pygame.init()

while True:
    conn, addr = skt.accept()
    print('connected by ' + str(addr))
    print('#######################')
    for key in CMD_DESCIBTIONS:
        print("###  "+CMD_DESCIBTIONS[key])
    print('#######################')
    while True:
        pressed_char = refrashPressedChar(pressed_char)
        if "P" == pressed_char:
            conn.sendall("P".encode("utf-8"))
            break;
        for in_char in pressed_char:
            for cmd in COMMAND_LIST:
                if cmd == in_char:
                    try:
                        cmd = cmd + "\n"
                        conn.sendall(cmd.encode("utf-8"))
                        print("Message send successfully")
                    except socket.error: 
                        print(socket.error.errno)
                        print('error sending')
        time.sleep(0.1)
    print('conn close!')
    conn.close()


