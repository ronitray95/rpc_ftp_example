#!/usr/bin/env python3

import os
from ftplib import *

FTP_URL = 'localhost'
FTP_PORT = 5000


def initFTP(cmd, *args):
    ftp = FTP()
    ftp.connect('localhost', FTP_PORT)
    resp = ftp.getwelcome()
    # print(resp)
    resp = ftp.login('user', '12345')
    # print(resp)

    fname = 'cmd.txt'
    with open(fname, 'w') as f:
        s = ''
        for arg in args:
            s = s + str(arg) + ' '
        f.write(cmd+' '+s)

    with open(fname, 'rb') as f:
        ftp.storbinary('STOR input.txt', f)

    ftp.retrbinary('RETR output.txt', open('userop.txt', 'wb').write)
    resp = ftp.sendcmd("QUIT")
    # print(resp)
    s = ''
    with open('userop.txt', 'r') as f:
        s = f.readline()
    os.remove('cmd.txt')
    os.remove('userop.txt')
    os.remove('input.txt')
    os.remove('output.txt')
    return s
