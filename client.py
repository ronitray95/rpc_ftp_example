#!/usr/bin/env python3

import rpc


z = rpc.initFTP('sumNumber', 5, 6, 7)
print(z)


z = rpc.initFTP('sum', 5, 6)
print(z)


z = rpc.initFTP('multiply', 5, 6, 7)
print(z)
