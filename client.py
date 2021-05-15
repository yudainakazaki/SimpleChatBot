import socket
import threading

format = 'utf-8'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_port = ('127.0.0.1', 8000)
# host_port = ('3.121.226.198', 5378)
s.connect(host_port)
print('Connected.')
print('Please type your username to login to the chat room.')


def receive():
    global s
    try:
        while True:
            temp = s.recv(1).decode(format)
            msg = temp
            while temp[-1] != '\n':
                temp = s.recv(1).decode(format)
                msg += temp
                
            if msg:
                if msg == 'IN-USE\n':
                    print('This username is already taken. Try with another one.\n')
                    s.close()
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(host_port)
                elif msg == 'BUSY\n':
                    print(msg)
                    print("Try again later!")
                    s.close()
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(host_port)
                else:
                    print(msg)
    except:
        s.close()


def write():
    try:
        while True:
            msg = input('') + '\n'
            # msg = input('') + '\n'
            # if msg == '!quit\n':
            #     s.sendall('QUIT\n'.encode(format))
            #     print('Leaving the room...')
            #     break
            if msg == '!quit\n':
                print('Leaving the room...')
                break
            elif msg == '!who\n':
                s.sendall('WHO\n'.encode(format))
            elif msg[0] == '@':
                parts = msg.split(' ', 1)
                username = parts[0][1:]
                if len(parts) == 1:
                    print("[Warning]Message body is null. Try again.\n")
                else:
                    message = parts[1]
                    send_msg = 'SEND' + ' ' + username + ' ' + message + '\n'
                    s.sendall(send_msg.encode(format))
            elif msg == '\n':
                continue
            else:
                entry_msg = "HELLO-FROM " + str(msg)
                # if entry_msg == "HELLO-FROM \n":
                #     print("[Warning]This username is not good.\n")
                # else:
                s.sendall(entry_msg.encode(format))
            
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        
    except:
        s.shutdown(socket.SHUT_RDWR)
        s.close()


receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
