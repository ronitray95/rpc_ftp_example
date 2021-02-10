#!/usr/bin/env python3

from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer

import os
import logging

mappings = {'old_method_name': 'new_method_name',
            'sumNumber': 'sum',
            'multiply': 'product',
            'prod': 'product',
            'divide': 'divide'
            }


class MyHandler(FTPHandler):

    def on_connect(self):
        print("%s:%s connected" % (self.remote_ip, self.remote_port))

    def on_disconnect(self):
        # do something when client disconnects
        pass

    def on_login(self, username):
        # do something when user login
        pass

    def on_logout(self, username):
        # do something when user logs out
        pass

    def on_file_sent(self, file):
        # do something when a file has been sent
        pass

    def on_file_received(self, file):
        # do something when a file has been received
        op = ''
        with open('input.txt', 'r') as f:
            line = (f.readline()).strip().split()
            cmd = line[0]
            print('ACTUAL CMD', cmd)
            if cmd not in mappings.keys() and cmd not in mappings.values():
                op = 'Unknown function'
            elif cmd in mappings.keys():
                op = globals()[mappings[cmd]](line[1:])
            else:
                op = globals()[cmd](line[1:])
        with open('output.txt', 'w') as f:
            f.write(op)

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        os.remove(file)


def sum(*args):
    print('Called sum', args[0])
    s = 0.0
    try:
        for arg in args[0]:
            s += float(arg)
        return str(s)
    except Exception:
        return 'Bad number format'


def product(*args):
    print('Called product', args[0])
    s = 1.0
    try:
        for arg in args[0]:
            s *= float(arg)
        return str(s)
    except Exception:
        return 'Bad number format'


def divide(*args):
    print('Called divide', args[0])
    if len(args) > 2:
        return 'Excess arguments'
    args = args[0]
    try:
        s = float(args[0]) / float(args[1])
        return str(s)
    except Exception:
        return 'Bad number format'


def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user('user', '12345', '.', perm='elradfmwMT')
    authorizer.add_anonymous('.', perm='elradfmwMT')

    handler = MyHandler
    handler.authorizer = authorizer

    # logging.basicConfig(level=logging.DEBUG)
    handler.banner = "pyftpdlib based ftpd ready."
    address = ('127.0.0.1', 5000)
    server = FTPServer(address, handler)
    server.max_cons = 256
    server.max_cons_per_ip = 5
    server.serve_forever()


if __name__ == '__main__':
    main()
