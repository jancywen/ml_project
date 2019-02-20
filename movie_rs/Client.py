# -*- coding: utf-8 -*-

import socket


ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.connect(('127.0.0.1', 9999))

ss.send('50'.encode('utf-8'))

buffer = []
while True:
    d = ss.recv(1024)
    # print(len(d))

    # print(d.decode('utf-8'))
    # print('---' * 10)
    if d and d.decode('utf-8') != 'end':
        buffer.append(d)
    else:
        break

data = b''.join(buffer)
# print(len(data))
print('*'*40)
print(data.decode('utf-8'))

ss.send('exit'.encode('utf-8'))
ss.close()
