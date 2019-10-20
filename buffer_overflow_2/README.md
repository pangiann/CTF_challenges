# Write-up for buffer-overflow-2 challenge
# PicoCTF_2018: buffer-overflow-2

**Category:** Binary Exploitation
**Points:** 250

> Alright, this time you'll need to control some arguments. Can you get the flag from this program? 
You can find it in /problems/buffer-overflow-2_1_63b4b691601811c553a7c19e367737b9 on the shell server. Source.

Let's run the program first:

```console
$ ./vuln
Please enter your string: 
AAAA
AAAA
```

Okay, we don't have anything useful.
It's time to disassemble the program.
 
I'll skip `main()` to go  straight to `vuln()`.

```asm
Dump of assembler code for function vuln:
   0x08048646 <+0>:	push   ebp
   0x08048647 <+1>:	mov    ebp,esp
   0x08048649 <+3>:	sub    esp,0x78
   0x0804864c <+6>:	sub    esp,0xc
   0x0804864f <+9>:	lea    eax,[ebp-0x6c]
   0x08048652 <+12>:	push   eax
   0x08048653 <+13>:	call   0x8048430 <gets@plt>
   0x08048658 <+18>:	add    esp,0x10
   0x0804865b <+21>:	sub    esp,0xc
   0x0804865e <+24>:	lea    eax,[ebp-0x6c]
   0x08048661 <+27>:	push   eax
   0x08048662 <+28>:	call   0x8048460 <puts@plt>
   0x08048667 <+33>:	add    esp,0x10
   0x0804866a <+36>:	nop
   0x0804866b <+37>:	leave  
   0x0804866c <+38>:	ret    
End of assembler dump.
```

We have the same vulnerability with buffer-overflow-2. 
Now, buffer's size is 0x6c (108 decimal).

Like the previous challenge there is a `win()` function that we want to return.
But, it wouldn't be enough for this challenge to jump to win function ofcourse.
Let's analyze them.

```asm
Dump of assembler code for function win:
   0x080485cb <+0>:	push   ebp
   0x080485cc <+1>:	mov    ebp,esp
   0x080485ce <+3>:	sub    esp,0x58
   0x080485d1 <+6>:	sub    esp,0x8
   0x080485d4 <+9>:	push   0x8048750
   0x080485d9 <+14>:	push   0x8048752
   0x080485de <+19>:	call   0x80484a0 <fopen@plt>
   0x080485e3 <+24>:	add    esp,0x10
   0x080485e6 <+27>:	mov    DWORD PTR [ebp-0xc],eax
   0x080485e9 <+30>:	cmp    DWORD PTR [ebp-0xc],0x0
   0x080485ed <+34>:	jne    0x8048609 <win+62>
   0x080485ef <+36>:	sub    esp,0xc
   0x080485f2 <+39>:	push   0x804875c
   0x080485f7 <+44>:	call   0x8048460 <puts@plt>
   0x080485fc <+49>:	add    esp,0x10
   0x080485ff <+52>:	sub    esp,0xc
   0x08048602 <+55>:	push   0x0
   0x08048604 <+57>:	call   0x8048470 <exit@plt>
   0x08048609 <+62>:	sub    esp,0x4
   0x0804860c <+65>:	push   DWORD PTR [ebp-0xc]
   0x0804860f <+68>:	push   0x40
   0x08048611 <+70>:	lea    eax,[ebp-0x4c]
   0x08048614 <+73>:	push   eax
   0x08048615 <+74>:	call   0x8048440 <fgets@plt>
   0x0804861a <+79>:	add    esp,0x10
   0x0804861d <+82>:	cmp    DWORD PTR [ebp+0x8],0xdeadbeef
   0x08048624 <+89>:	jne    0x8048640 <win+117>
   0x08048626 <+91>:	cmp    DWORD PTR [ebp+0xc],0xdeadc0de
   0x0804862d <+98>:	jne    0x8048643 <win+120>
   0x0804862f <+100>:	sub    esp,0xc
   0x08048632 <+103>:	lea    eax,[ebp-0x4c]
   0x08048635 <+106>:	push   eax
   0x08048636 <+107>:	call   0x8048420 <printf@plt>
   0x0804863b <+112>:	add    esp,0x10
   0x0804863e <+115>:	jmp    0x8048644 <win+121>
   0x08048640 <+117>:	nop
   0x08048641 <+118>:	jmp    0x8048644 <win+121>
   0x08048643 <+120>:	nop
   0x08048644 <+121>:	leave  
   0x08048645 <+122>:	ret    
End of assembler dump.
```

In the first lines, program opens flag.txt file but we see 2 very important lines:

```asm
   0x0804861d <+82>:	cmp    DWORD PTR [ebp+0x8],0xdeadbeef
   0x08048624 <+89>:	jne    0x8048640 <win+117>
   0x08048626 <+91>:	cmp    DWORD PTR [ebp+0xc],0xdeadc0de
   0x0804862d <+98>:	jne    0x8048643 <win+120>
```

First of all, we have to clear something. If you know how C programs lie in memory you would see that `win()` function takes two arguments
. These values are stored at ebp + 0x8 and ebp + 0xc (ebp + 0x10 if there  were more etc.). 

So, to print the flag arg1 must be 0xdeadbeef and arg2 0xdeadc0de.

How could we intervene to those values?

Think about it...
Before we call RET instruction inside `vuln` ontains X address and program is at address X + 0x4.  We've changed return address in order to jump to `win`.
With ret instruction we pop return address from stack, so now inside rbp we find X + 0x4. 
Then, prolog of `win` function comes:
```asm
0x080485cb <+0>:	push   ebp
0x080485cc <+1>:	mov    ebp,esp
```

We push ebp, so 



