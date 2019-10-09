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

Confirm by listing the file with ls -l vuln flag.txt. The result have to be something like that:
```
-r--r----- 1 root root 35 Oct 5 00:27 flag.txt
-rwxr-sr-x root root 725472 Oct 5 00:23 vuln
```
As you can see flag's and vuln's group ownership is root. But our user is not in root's group unfortunately. As you can see flag.txt 
 readable only from owner(root) and the members of the group's ownership(root again). 




