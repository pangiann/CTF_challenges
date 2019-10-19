# Write-up for be-quick-or-be-dead-2 challenge
# PicoCTF_2018: be-quick-or-be-dead-2

**Category:** Reversing
**Points:** 275

> As you enjoy this [music](https://www.youtube.com/watch?v=CTt1vk9nM9c) even more, another executable 
**be-quick-or-be-dead-2** shows up. Can you run this fast enough too?

Let's run the binary:

```console

user@user:~/ ./be-quick-or-be-dead-2

Be Quick Or Be Dead 2
=====================

Calculating key...
You need a faster machine. Bye bye.
```

Time to analyze the binary with gdb. We don't have any info right now.

```asm
Dump of assembler code for function main:
   0x000000000040085f <+0>:	push   rbp
   0x0000000000400860 <+1>:	mov    rbp,rsp
   0x0000000000400863 <+4>:	sub    rsp,0x10
   0x0000000000400867 <+8>:	mov    DWORD PTR [rbp-0x4],edi
   0x000000000040086a <+11>:	mov    QWORD PTR [rbp-0x10],rsi
   0x000000000040086e <+15>:	mov    eax,0x0
   0x0000000000400873 <+20>:	call   0x400821 <header>
   0x0000000000400878 <+25>:	mov    eax,0x0
   0x000000000040087d <+30>:	call   0x40077a <set_timer>
   0x0000000000400882 <+35>:	mov    eax,0x0
   0x0000000000400887 <+40>:	call   0x4007ce <get_key>
   0x000000000040088c <+45>:	mov    eax,0x0
   0x0000000000400891 <+50>:	call   0x4007f9 <print_flag>
   0x0000000000400896 <+55>:	mov    eax,0x0
   0x000000000040089b <+60>:	leave  
   0x000000000040089c <+61>:	ret    
End of assembler dump.

```

The `main` function is similar to be-quick-or-be-dead-1.
However, this time disabling the time will not do the job. We hand and the program does not return in a reasonable time.

Like last time, the `get_key` function calls the `calculate_key` function where gold hides there.
Analyzing get_key function we get this:
```asm
Dump of assembler code for function get_key:
   0x00000000004007ce <+0>:	push   rbp
   0x00000000004007cf <+1>:	mov    rbp,rsp
   0x00000000004007d2 <+4>:	mov    edi,0x4009b8
   0x00000000004007d7 <+9>:	call   0x400530 <puts@plt>
   0x00000000004007dc <+14>:	mov    eax,0x0
   0x00000000004007e1 <+19>:	call   0x40074b <calculate_key>
   0x00000000004007e6 <+24>:	mov    DWORD PTR [rip+0x2008d4],eax        # 0x6010c0 <key>
   0x00000000004007ec <+30>:	mov    edi,0x4009cb
   0x00000000004007f1 <+35>:	call   0x400530 <puts@plt>
   0x00000000004007f6 <+40>:	nop
   0x00000000004007f7 <+41>:	pop    rbp
   0x00000000004007f8 <+42>:	ret    
End of assembler dump.
```

**calculate_key**  probably delays us.

```asm
Dump of assembler code for function calculate_key:
   0x000000000040074b <+0>:	push   rbp
   0x000000000040074c <+1>:	mov    rbp,rsp
   0x000000000040074f <+4>:	mov    edi,0x402
   0x0000000000400754 <+9>:	call   0x400706 <fib>
   0x0000000000400759 <+14>:	pop    rbp
   0x000000000040075a <+15>:	ret    
End of assembler dump.

```


This function calls `fib` with 0x402 (1026 in decimal) as a parameter.
`fib` calculates the nth member of the Fibonacci series.

Sadly, it's a very slow and bad implementation and it takes a lot of time.
So, we create a much better version and calculate the fib(1026)
```python
def fibonacci(n): 
	a = 0
	b = 1
	if n < 0: 
		print("Incorrect input") 
	elif n == 0: 
		return a & 0xffffffff
	elif n == 1: 
		return b & 0xffffffff
	else: 
		for i in range(2,n+1): 
			c = a + b 
			a = b 
			b = c 
		return b & 0xffffffff


print(fibonacci(1026)) 
```
Note that we use & 0xffffffff in order to simulate the overflows that occur when adding 32-bit integers (as in the original assembly).

The result is stored in eax.
```console
user@user:~/ python fibo1.py
4144667480
```

We want to change this instruction: 
```asm
0x00000000004007e1 <+19>:	call   0x40074b <calculate_key>
```

with: 
```asm
mov eax, 4144667480 
```
Following the same procedure as in the last challenge we patch the code.


With radare2 and rasm2 command we convert instruction to hex code.
```console
user@user:~/ rasm2 'mov eax,  4144667480'

b8589b0af7
```


At virtual address 0x00000000004007e1 we would like to insert 0xb8589b0af7. We have to  find first the offset in the binary itself.

```console
user@user:~/ objdump -t be-quick-or-be-dead-2

be-quick-or-be-dead-2:     file format elf64-x86-64

SYMBOL TABLE:
0000000000400238 l    d  .interp	0000000000000000              .interp
0000000000400254 l    d  .note.ABI-tag	0000000000000000              .note.ABI-tag
0000000000400274 l    d  .note.gnu.build-id	0000000000000000              .note.gnu.build-id
0000000000400298 l    d  .gnu.hash	0000000000000000              .gnu.hash
00000000004002b8 l    d  .dynsym	0000000000000000              .dynsym
0000000000400390 l    d  .dynstr	0000000000000000              .dynstr
00000000004003f6 l    d  .gnu.version	0000000000000000              .gnu.version
0000000000400408 l    d  .gnu.version_r	0000000000000000              .gnu.version_r
0000000000400428 l    d  .rela.dyn	0000000000000000              .rela.dyn
0000000000400440 l    d  .rela.plt	0000000000000000              .rela.plt
00000000004004e8 l    d  .init	0000000000000000              .init
0000000000400510 l    d  .plt	0000000000000000              .plt
0000000000400590 l    d  .plt.got	0000000000000000              .plt.got
00000000004005a0 l    d  .text	0000000000000000              .text
0000000000400914 l    d  .fini	0000000000000000              .fini
.
.
.
```
Our code starts at 00000000004005a0 and our instruction is at 0x00000000004007e1. 


```console
user@user:~/ readelf --wide -S be-quick-or-be-dead-1
There are 31 section headers, starting at offset 0x1ca8:

Section Headers:
  [Nr] Name              Type            Address          Off    Size   ES Flg Lk Inf Al
  [ 0]                   NULL            0000000000000000 000000 000000 00      0   0  0
  [ 1] .interp           PROGBITS        0000000000400238 000238 00001c 00   A  0   0  1
  [ 2] .note.ABI-tag     NOTE            0000000000400254 000254 000020 00   A  0   0  4
  [ 3] .note.gnu.build-id NOTE            0000000000400274 000274 000024 00   A  0   0  4
  [ 4] .gnu.hash         GNU_HASH        0000000000400298 000298 00001c 00   A  5   0  8
  [ 5] .dynsym           DYNSYM          00000000004002b8 0002b8 0000d8 18   A  6   1  8
  [ 6] .dynstr           STRTAB          0000000000400390 000390 000065 00   A  0   0  1
  [ 7] .gnu.version      VERSYM          00000000004003f6 0003f6 000012 02   A  5   0  2
  [ 8] .gnu.version_r    VERNEED         0000000000400408 000408 000020 00   A  6   1  8
  [ 9] .rela.dyn         RELA            0000000000400428 000428 000018 18   A  5   0  8
  [10] .rela.plt         RELA            0000000000400440 000440 0000a8 18  AI  5  24  8
  [11] .init             PROGBITS        00000000004004e8 0004e8 00001a 00  AX  0   0  4
  [12] .plt              PROGBITS        0000000000400510 000510 000080 10  AX  0   0 16
  [13] .plt.got          PROGBITS        0000000000400590 000590 000008 00  AX  0   0  8
  [14] .text             PROGBITS        00000000004005a0 0005a0 000372 00  AX  0   0 16
  [15] .fini             PROGBITS        0000000000400914 000914 000009 00  AX  0   0  4
  [16] .rodata           PROGBITS        0000000000400920 000920 0000e8 00   A  0   0 16
  [17] .eh_frame_hdr     PROGBITS        0000000000400a08 000a08 000074 00   A  0   0  4
  [18] .eh_frame         PROGBITS        0000000000400a80 000a80 0001f4 00   A  0   0  8
  [19] .init_array       INIT_ARRAY      0000000000600e10 000e10 000008 00  WA  0   0  8
  [20] .fini_array       FINI_ARRAY      0000000000600e18 000e18 000008 00  WA  0   0  8
  [21] .jcr              PROGBITS        0000000000600e20 000e20 000008 00  WA  0   0  8
  [22] .dynamic          DYNAMIC         0000000000600e28 000e28 0001d0 10  WA  6   0  8
  [23] .got              PROGBITS        0000000000600ff8 000ff8 000008 08  WA  0   0  8
  [24] .got.plt          PROGBITS        0000000000601000 001000 000050 08  WA  0   0  8
  [25] .data             PROGBITS        0000000000601060 001060 00005a 00  WA  0   0 32
  [26] .bss              NOBITS          00000000006010bc 0010ba 00000c 00  WA  0   0  4
  [27] .comment          PROGBITS        0000000000000000 0010ba 000035 01  MS  0   0  1
  [28] .shstrtab         STRTAB          0000000000000000 001b9c 00010c 00      0   0  1
  [29] .symtab           SYMTAB          0000000000000000 0010f0 0007c8 18     30  47  8
  [30] .strtab           STRTAB          0000000000000000 0018b8 0002e4 00      0   0  1
Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings), I (info),
  L (link order), O (extra OS processing required), G (group), T (TLS),
  C (compressed), x (unknown), o (OS specific), E (exclude),
  l (large), p (processor specific)
```
We can see that offset of .text is 0005a0 so instruction's offset is:
```
 00000000004005a0 - 0x0005a0 + 0x00000000004007e1 = 0x0007e1
 ```
 
> # Crafting the script

```bash
#!/bin/bash

cp -p be-quick-or-be-dead-2 be-quick-or-be-dead-2_patched
chmod +x be-quick-or-be-dead-2_patched
rasm2 'mov eax, 4144667480' | xxd -p -r | dd conv=notrunc of=be-quick-or-be-dead-2_patched bs=1 seek=$((0x7e1)) 2>/dev/null
./be-quick-or-be-dead-2_patched | tail -1
```


Congrats! We did it. 
