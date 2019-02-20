# -*- coding: utf-8 -*-

import socket
import threading
import time
import codecs


ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('127.0.0.1', 9999))
ss.listen(5)

print('HTTP Start...')

inc = 0

def tcpLink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    # sock.send(b'Welcome!')

    while True:
        data = sock.recv(1024)
        time.sleep(0.5)
        if not data or data.decode('utf-8') == 'exit':
            break


        # print(data.decode('utf-8'))

        m = Movie()
        # print(m.movic_list)

        # http_response = m.movic_list[data.decode('utf-8')]
        http_response = m.detail_fp(data.decode('utf-8'))
        sock.send(http_response.encode('utf-8'))
        # sock.send(','.join(http_response).encode('utf-8'))
        # sock.send(('Hello, %s' % data.decode('utf-8')).encode('utf-8'))
        time.sleep(0.5)
        sock.send('end'.encode('utf-8'))

    sock.close()



class Movie():

    movic_list = {}

    related = {}
    related_fp = {}
    movice = {}
    def __init__(self):
        with open('./ml-100k/u1.base') as f:
            for line in f.readlines():
                ls = line.strip().split('\t')

                if ls[0] not in self.movic_list:
                    self.movic_list[ls[0]] = []
                self.movic_list[ls[0]].append('&&'.join(ls[1:]))

        with codecs.open("./ml-100k/u.item", 'r', encoding="ISO-8859-1") as f:
            for line in f.readlines():
                ls = line.split('|')
                self.movice[ls[0]] = '&&'.join(ls[1:])

        with open('./result_fp') as f:
            for line in f.readlines():
                ls = line.strip().split('&&')
                if ls[0] not in self.related_fp:
                    self.related_fp[ls[0]] = []
                self.related_fp[ls[0]] += ls[1:]


    def check(self, movieId):
        if movieId in self.movice.keys():
            return self.movice[movieId]
        return 'Not Found'


    def find_related(self, movieId):
        if movieId in self.related.keys():
            return self.related[movieId]
        return 'Not Found'

    def detail(self, movieId):
        ret = ''
        if movieId in self.related.keys():
            ids = self.related[movieId].split('&&')
            for idss in ids:
                ret += self.check(idss)
                ret += '\r\n'
        return ret

    def detail_fp(self, movieId):
        print('movie_id:')
        print(movieId)
        print('related_fp:')
        print(self.related_fp)

        ret = ''
        if movieId in self.related_fp.keys():
            ids = set(self.related_fp[movieId])
            for idss in ids:
                ret += self.check(idss)
                ret += '\r\n'
        return ret

while True:
    sock, addr = ss.accept()

    t = threading.Thread(target=tcpLink, args=(sock, addr))
    t.start()


