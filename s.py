import socket 
import threading

format = 'utf-8'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_port = ('127.0.0.1', 8000)

s.bind(host_port)
print('Server established!!\n')
s.listen()

usernames = []
clients = []

def receive_message(client):
    while True:
        try:
            # temp = client.recv(1).decode(format)
            # msg = temp
            # while temp[-1] != '\n':
            #     temp = client.recv(1).decode(format)
            #     msg += temp
            msg = client.recv(4096).decode(format)
            header = msg.split(' ', 1)[0]
            for c in clients:
                if c != client:
                    try:
                        i = clients.index(c)
                        # print (usernames[i])
                        c.sendall("".encode(format))
                    except:
                        c.close()
                        # print("hello")
                        i = clients.index(c)
                        del usernames[i]
                        clients.remove(c)
            if header == 'WHO\n':
                # print(f"Send the member list to {client}")
                list = ', '.join(usernames)
                list = list + '\n'
                reply = 'WHO-OK ' + list
                client.send(reply.encode(format))
            elif header == 'SEND':
                msg_parts = msg.split(' ', 2)
                dest_user = msg_parts[1]
                if dest_user in usernames:
                    try:
                        print('Send message to {}'.format(dest_user))
                        client_index = clients.index(client)
                        client_username = usernames[client_index]
                        msg_to_user = 'DELIVERY' + ' ' + client_username + ' ' + msg_parts[2] + '\n'
                        index = usernames.index(dest_user)
                        dest_client = clients[index]
                        dest_client.sendall(msg_to_user.encode(format))
                        reply = 'SEND-OK\n'
                        client.sendall(reply.encode(format))
                    except:
                        error_msg = 'BAD-RQST-BODY\n'
                        client.sendall(error_msg.encode(format))
                else:
                    reply = 'UNKNOWN\n'
                    client.sendall(reply.encode(format))

            elif header == 'QUIT\n':
                index = clients.index(client)
                clients.remove(client)
                username = usernames[index]
                usernames.remove(username)
                print('{} left the room.'.format(username).encode(format))
                print('Current member: ' + str(usernames))
                
            else:
                client.sendall('BAD-RQST-HDR\n'.encode(format))
                
        except:
            pass
    

def receive():
    try:
        while True:
            client, address = s.accept()
            print('Connected with {}'.format(str(address)))
            msg = client.recv(1024).decode(format)
            if len(usernames) == 3:
                print("Over capacity.")
                client.sendall('BUSY\n'.encode(format))
            else: 
                header = msg.split(' ', 2)[0]
                # msg_body = msg.split(' ', 2)[1]
                if header == 'HELLO-FROM':
                    try:
                        parts = msg.split(' ', 1)
                        username = parts[1][:-1]
                        uniq = True
                        for i in usernames:
                            if i == username:
                                uniq = False
                                break
                        if uniq == False:
                            print('The username sent from the client was not unique.')
                            client.sendall('IN-USE\n'.encode(format))
                        elif uniq == True:
                            print(username)
                            reply = 'HELLO ' + username + '\n'
                            client.sendall(reply.encode(format))
                            usernames.append(username)
                            clients.append(client)
                            print('Current member: ' + str(usernames))
                    except:
                        error_msg = 'BAD-RQST-BODY\n'
                        client.send(error_msg.encode(format))
                            
                else:
                    error_msg = 'BAD-RQST-HDR\n'
                    client.send(error_msg.encode(format))

            thread = threading.Thread(target=receive_message, args=(client,))
            thread.start()
            
            
    except Exception:
        s.close()
        
    
receive()
# thread = threading.Thread(target=receive)
# thread.start()
    