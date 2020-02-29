section .text
            global _start
 
    _start:
            xor     rdx, rdx                ; clearing rdx register 
            mov     qword rbx, '//bin/sh'   ; pushing //bin/sh to rbx register
            shr     rbx, 0x8                ; shift right 8 times rbx register (I'll explain it below)
            push    rbx                     ; push /bin/sh in stack
            mov     rdi, rsp                ; rdi now has address of /bin/sh
			xor     rax, rax
            push    rax                     ; pushing NULL byte
            push    rdi                     ; pushing address of /bin/sh
            mov     rsi, rsp                ; rsi has now address of address of /bin/sh
            mov     al, 0x3b                ; syscall number of execve is 59 in 64bit systems
            syscall   
