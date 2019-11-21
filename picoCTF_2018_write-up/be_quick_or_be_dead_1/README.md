# Write-up for be-quick-or-be-dead-1 challenge
# PicoCTF_2018: be-quick-or-be-dead-1

**Category:** Reversing
**Points:** 200

> You find [this](https://www.youtube.com/watch?v=CTt1vk9nM9c) when searching for some music, 
which leads you to **be-quick-or-be-dead-1**. Can you run it fast enough?

Let's run the binary:

```console

user@user:~/ ./be-quick-or-be-dead-1

Be Quick Or Be Dead 1
=====================

Calculating key...
You need a faster machine. Bye bye.
```

Time to analyze the binary with gdb. We don't have any info right now.

```asm
Dump of assembler code for function main:
   0x0000000000400827 <+0>:	push   rbp
   0x0000000000400828 <+1>:	mov    rbp,rsp
   0x000000000040082b <+4>:	sub    rsp,0x10
   0x000000000040082f <+8>:	mov    DWORD PTR [rbp-0x4],edi
   0x0000000000400832 <+11>:	mov    QWORD PTR [rbp-0x10],rsi
   0x0000000000400836 <+15>:	mov    eax,0x0
   0x000000000040083b <+20>:	call   0x4007e9 <header>
   0x0000000000400840 <+25>:	mov    eax,0x0
   0x0000000000400845 <+30>:	call   0x400742 <set_timer>
   0x000000000040084a <+35>:	mov    eax,0x0
   0x000000000040084f <+40>:	call   0x400796 <get_key>
   0x0000000000400854 <+45>:	mov    eax,0x0
   0x0000000000400859 <+50>:	call   0x4007c1 <print_flag>
   0x000000000040085e <+55>:	mov    eax,0x0
   0x0000000000400863 <+60>:	leave  
   0x0000000000400864 <+61>:	ret    
End of assembler dump.
```


Okay, we have a function called header. Probably header is there to print the first two lines of the output.
After that, **set_timer** puts us in a time limitation. We need to execute rest of the code before time limit.
(After 1 second the alarm handler will be triggered and terminate the program)
Now, we  do not achieve this. 
Analyzing get_key function we get this:
```asm
Dump of assembler code for function get_key:
   0x0000000000400796 <+0>:	push   rbp
   0x0000000000400797 <+1>:	mov    rbp,rsp
   0x000000000040079a <+4>:	mov    edi,0x400988
   0x000000000040079f <+9>:	call   0x400530 <puts@plt>
   0x00000000004007a4 <+14>:	mov    eax,0x0
   0x00000000004007a9 <+19>:	call   0x400706 <calculate_key>
   0x00000000004007ae <+24>:	mov    DWORD PTR [rip+0x20090c],eax        # 0x6010c0 <key>
   0x00000000004007b4 <+30>:	mov    edi,0x40099b
   0x00000000004007b9 <+35>:	call   0x400530 <puts@plt>
   0x00000000004007be <+40>:	nop
   0x00000000004007bf <+41>:	pop    rbp
   0x00000000004007c0 <+42>:	ret    
End of assembler dump.
```

**calculate_key**  probably delays us.

```asm
Dump of assembler code for function calculate_key:
   0x0000000000400706 <+0>:	push   rbp
   0x0000000000400707 <+1>:	mov    rbp,rsp
   0x000000000040070a <+4>:	mov    DWORD PTR [rbp-0x4],0x75c3328b
   0x0000000000400711 <+11>:	add    DWORD PTR [rbp-0x4],0x1
   0x0000000000400715 <+15>:	cmp    DWORD PTR [rbp-0x4],0xeb866516
   0x000000000040071c <+22>:	jne    0x400711 <calculate_key+11>
   0x000000000040071e <+24>:	mov    eax,DWORD PTR [rbp-0x4]
   0x0000000000400721 <+27>:	pop    rbp
   0x0000000000400722 <+28>:	ret    
End of assembler dump.
```

That's a very bad code definitely. It's a big loop that takes a lot of time and we miss the flag.

What if we  move to eax the result ( which is 0xeb866516 ) straight and skip this useless loop?
Let's do it inside gdb and then we will craft a bash script outside disassembler.

We want to change this instruction: 
```asm
0x00000000004007a9 <+19>:	call   0x400706 <calculate_key>
```

with: 
```asm
mov eax,  0xeb866516
```
That's seems difficult but it's not. 
We need to convert this instruction with hex value of it. Then, we can put those values inside 0x00000000004007a9 and that's it.

There are two ways to convert this instruction to hex code.
  - Create asm file (instruction.asm) with the code inside.
  - nasm -f elf64 instruction.asm
  - objdump -d instruction.o

And you get the hex values.
Otherwise, with radare2 and rasm2 command it's much easier, so:
```console
user@user:~/ rasm2 'mov eax,  0xeb866516'

b8166586eb
```

We get back to gdb:

```gdb
Breakpoint 1, 0x0000000000400827 in main ()
=> 0x0000000000400827 <main+0>:	55	push   rbp
(gdb) set {char[5]} 0x00000000004007a9 = {0xb8, 0x16, 0x65, 0x86, 0xeb}
(gdb) x/2wx 0x00000000004007a9
0x4007a9 <get_key+19>:	0x866516b8	0x0c0589eb
(gdb) disas get_key
Dump of assembler code for function get_key:
   0x0000000000400796 <+0>:	push   rbp
   0x0000000000400797 <+1>:	mov    rbp,rsp
   0x000000000040079a <+4>:	mov    edi,0x400988
   0x000000000040079f <+9>:	call   0x400530 <puts@plt>
   0x00000000004007a4 <+14>:	mov    eax,0x0
   0x00000000004007a9 <+19>:	mov    eax,0xeb866516
   0x00000000004007ae <+24>:	mov    DWORD PTR [rip+0x20090c],eax        # 0x6010c0 <key>
   0x00000000004007b4 <+30>:	mov    edi,0x40099b
   0x00000000004007b9 <+35>:	call   0x400530 <puts@plt>
   0x00000000004007be <+40>:	nop
   0x00000000004007bf <+41>:	pop    rbp
   0x00000000004007c0 <+42>:	ret    
End of assembler dump.
(gdb) c
Continuing.
Be Quick Or Be Dead 1
=====================

Calculating key...
Done calculating key
Printing flag:
picoCTF{why_bother_doing_unnecessary_computation_402ca676}
[Inferior 1 (process 7056) exited normally]
(gdb) 

```

PERFECT, we got our flag.
Time to do it outside gdb because WE CAN.

At virtual address 0x00000000004007a9 we would like to replace 0xe858ffffff with 0xb8166586eb. We want to find the offset in the binary itself.

We will need to check the section table of the executable:

```console
user@user:~/ objdump -t be-quick-or-be-dead-1

be-quick-or-be-dead-1:     file format elf64-x86-64

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
00000000004008e4 l    d  .fini	0000000000000000              .fini
.
.
.
```
Our code starts at 00000000004005a0 and our instruction is at 0x00000000004007a9. 

```console
user@user:~/ readelf --wide -S be-quick-or-be-dead-1
There are 31 section headers, starting at offset 0x1c90:

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
  [14] .text             PROGBITS        00000000004005a0 0005a0 000342 00  AX  0   0 16
  [15] .fini             PROGBITS        00000000004008e4 0008e4 000009 00  AX  0   0  4
  [16] .rodata           PROGBITS        00000000004008f0 0008f0 0000e8 00   A  0   0 16
  [17] .eh_frame_hdr     PROGBITS        00000000004009d8 0009d8 00006c 00   A  0   0  4
  [18] .eh_frame         PROGBITS        0000000000400a48 000a48 0001d4 00   A  0   0  8
  [19] .init_array       INIT_ARRAY      0000000000600e10 000e10 000008 00  WA  0   0  8
  [20] .fini_array       FINI_ARRAY      0000000000600e18 000e18 000008 00  WA  0   0  8
  [21] .jcr              PROGBITS        0000000000600e20 000e20 000008 00  WA  0   0  8
  [22] .dynamic          DYNAMIC         0000000000600e28 000e28 0001d0 10  WA  6   0  8
  [23] .got              PROGBITS        0000000000600ff8 000ff8 000008 08  WA  0   0  8
  [24] .got.plt          PROGBITS        0000000000601000 001000 000050 08  WA  0   0  8
  [25] .data             PROGBITS        0000000000601060 001060 00005b 00  WA  0   0 32
  [26] .bss              NOBITS          00000000006010bc 0010bb 00000c 00  WA  0   0  4
  [27] .comment          PROGBITS        0000000000000000 0010bb 000035 01  MS  0   0  1
  [28] .shstrtab         STRTAB          0000000000000000 001b80 00010c 00      0   0  1
  [29] .symtab           SYMTAB          0000000000000000 0010f0 0007b0 18     30  47  8
  [30] .strtab           STRTAB          0000000000000000 0018a0 0002e0 00      0   0  1
Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings), I (info),
  L (link order), O (extra OS processing required), G (group), T (TLS),
  C (compressed), x (unknown), o (OS specific), E (exclude),
  l (large), p (processor specific)
```
We can see that offset of .text is 0005a0 so instruction's offset is:
```
 00000000004005a0 - 0x0005a0 + 0x00000000004007a9 = 0x0007a9
 ```
 
That's it we know everything to patch this program. 
```bash
#!/bin/bash

cp be-quick-or-be-dead-1 be-quick-or-be-dead-1_patched
chmod +x be-quick-or-be-dead-1_patched

rasm2 'mov eax, 0xeb866516' | xxd -p -r | dd conv=notrunc of=be-quick-or-be-dead-1_patched bs=1 seek=$((0x7a9)) 2>/dev/null
# xxd with -r option converts hex to binary and with -p prints it to the stdout
# dd just edits the binary
./be-quick-or-be-dead-1_patched | tail -1 
```
More about dd see [here](https://www.geeksforgeeks.org/dd-command-linux/) and in the [man page](http://man7.org/linux/man-pages/man1/dd.1.html).

Congrats! We did it. 



 
