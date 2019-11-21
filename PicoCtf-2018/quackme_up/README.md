# Write-up for quackme_up challenge
# PicoCTF_2018: quackme up

**Category:** Reversing
**Points:** 350

>The duck puns continue. Can you crack, I mean quack this program as well? 
You can find the program in /problems/quackme-up_2_bf9649c854a2615a35ccdc3660a31602 on the shell server.

First of all, let's execute the program:

```console
user@user:~/$ ./main

We're moving along swimmingly. Is this one too fowl for you?
Enter text to encrypt: [input]
Here's your ciphertext: [output]
Now quack it! : 11 80 20 E0 22 53 72 A1 01 41 55 20 A0 C0 25 E3 35 40 65 95 75 00 30 85 C1
That's all folks.
```

Okay, maybe we have to crack some ciphertext.
I tried as input: **picoCTF** and I got the following:
```console
user@user:~/$ ./main

We're moving along swimmingly. Is this one too fowl for you?
Enter text to encrypt: picoCTF
Here's your ciphertext: 11 80 20 E0 22 53 72
Now quack it! : 11 80 20 E0 22 53 72 A1 01 41 55 20 A0 C0 25 E3 35 40 65 95 75 00 30 85 C1
That's all folks.
```
We see that these hex values given are our flag.
Basically, we need to find how program encrypts our input in order to decrypt those values to get the flag.
Now we disassemble the program in gdb:

```asm
Dump of assembler code for function main:
   0x080486f6 <+0>:	lea    ecx,[esp+0x4]
   0x080486fa <+4>:	and    esp,0xfffffff0
   0x080486fd <+7>:	push   DWORD PTR [ecx-0x4]
   0x08048700 <+10>:	push   ebp
   0x08048701 <+11>:	mov    ebp,esp
   0x08048703 <+13>:	push   ecx
   0x08048704 <+14>:	sub    esp,0x14
   0x08048707 <+17>:	sub    esp,0xc
   0x0804870a <+20>:	push   0x8048884
   0x0804870f <+25>:	call   0x8048400 <puts@plt>
   0x08048714 <+30>:	add    esp,0x10
   0x08048717 <+33>:	sub    esp,0xc
   0x0804871a <+36>:	push   0x80488c1
   0x0804871f <+41>:	call   0x80483e0 <printf@plt>
   0x08048724 <+46>:	add    esp,0x10
   0x08048727 <+49>:	call   0x804854b <read_input>
   0x0804872c <+54>:	mov    DWORD PTR [ebp-0x10],eax
   0x0804872f <+57>:	sub    esp,0xc
   0x08048732 <+60>:	push   DWORD PTR [ebp-0x10]
   0x08048735 <+63>:	call   0x804867f <encrypt>
   0x0804873a <+68>:	add    esp,0x10
   0x0804873d <+71>:	mov    DWORD PTR [ebp-0xc],eax
   0x08048740 <+74>:	sub    esp,0xc
   0x08048743 <+77>:	push   0x80488d9
   0x08048748 <+82>:	call   0x80483e0 <printf@plt>
   0x0804874d <+87>:	add    esp,0x10
   0x08048750 <+90>:	sub    esp,0x8
   0x08048753 <+93>:	push   DWORD PTR [ebp-0xc]
   0x08048756 <+96>:	push   DWORD PTR [ebp-0x10]
   0x08048759 <+99>:	call   0x804861f <print_hex>
   0x0804875e <+104>:	add    esp,0x10
   0x08048761 <+107>:	mov    eax,ds:0x804a030
   0x08048766 <+112>:	sub    esp,0x8
   0x08048769 <+115>:	push   eax
   0x0804876a <+116>:	push   0x80488f2
   0x0804876f <+121>:	call   0x80483e0 <printf@plt>
   0x08048774 <+126>:	add    esp,0x10
   0x08048777 <+129>:	sub    esp,0xc
   0x0804877a <+132>:	push   0x8048906
   0x0804877f <+137>:	call   0x8048400 <puts@plt>
   0x08048784 <+142>:	add    esp,0x10
   0x08048787 <+145>:	mov    eax,0x0
   0x0804878c <+150>:	mov    ecx,DWORD PTR [ebp-0x4]
   0x0804878f <+153>:	leave  
   0x08048790 <+154>:	lea    esp,[ecx-0x4]
   0x08048793 <+157>:	ret    
End of assembler dump.
```

The most interesting part here seems to be encrypt() function. Let's inspect it:
```asm
Dump of assembler code for function encrypt:
   0x0804867f <+0>:	push   ebp
   0x08048680 <+1>:	mov    ebp,esp
   0x08048682 <+3>:	sub    esp,0x18
   0x08048685 <+6>:	sub    esp,0xc
   0x08048688 <+9>:	push   DWORD PTR [ebp+0x8]
   0x0804868b <+12>:	call   0x8048410 <strlen@plt>
   0x08048690 <+17>:	add    esp,0x10
   0x08048693 <+20>:	mov    DWORD PTR [ebp-0xc],eax
   0x08048696 <+23>:	mov    DWORD PTR [ebp-0x10],0x0
   0x0804869d <+30>:	jmp    0x80486e9 <encrypt+106>
   0x0804869f <+32>:	mov    edx,DWORD PTR [ebp-0x10]
   0x080486a2 <+35>:	mov    eax,DWORD PTR [ebp+0x8]
   0x080486a5 <+38>:	add    eax,edx
   0x080486a7 <+40>:	movzx  eax,BYTE PTR [eax]
   0x080486aa <+43>:	mov    BYTE PTR [ebp-0x11],al
   0x080486ad <+46>:	movsx  eax,BYTE PTR [ebp-0x11]
   0x080486b1 <+50>:	sub    esp,0xc
   0x080486b4 <+53>:	push   eax
   0x080486b5 <+54>:	call   0x80485d1 <rol4>
   0x080486ba <+59>:	add    esp,0x10
   0x080486bd <+62>:	mov    BYTE PTR [ebp-0x11],al
   0x080486c0 <+65>:	xor    BYTE PTR [ebp-0x11],0x16
   0x080486c4 <+69>:	movsx  eax,BYTE PTR [ebp-0x11]
   0x080486c8 <+73>:	sub    esp,0xc
   0x080486cb <+76>:	push   eax
   0x080486cc <+77>:	call   0x80485f8 <ror8>
   0x080486d1 <+82>:	add    esp,0x10
   0x080486d4 <+85>:	mov    BYTE PTR [ebp-0x11],al
   0x080486d7 <+88>:	mov    edx,DWORD PTR [ebp-0x10]
   0x080486da <+91>:	mov    eax,DWORD PTR [ebp+0x8]
   0x080486dd <+94>:	add    edx,eax
   0x080486df <+96>:	movzx  eax,BYTE PTR [ebp-0x11]
   0x080486e3 <+100>:	mov    BYTE PTR [edx],al
   0x080486e5 <+102>:	add    DWORD PTR [ebp-0x10],0x1
   0x080486e9 <+106>:	mov    eax,DWORD PTR [ebp-0x10]
   0x080486ec <+109>:	cmp    eax,DWORD PTR [ebp-0xc]
   0x080486ef <+112>:	jl     0x804869f <encrypt+32>
   0x080486f1 <+114>:	mov    eax,DWORD PTR [ebp-0xc]
   0x080486f4 <+117>:	leave  
   0x080486f5 <+118>:	ret    
End of assembler dump.

   0x080486f5 <+118>:	ret    
End of assembler dump.
```

In general, our eye should go to the function calls and jumps to understand the code (see the bigger picture). 
Running the program in gdb we notice a loop. At the bottom of the assembly code we can see the condition checking.
```asm
   0x080486e5 <+102>:	add    DWORD PTR [ebp-0x10],0x1
   0x080486e9 <+106>:	mov    eax,DWORD PTR [ebp-0x10]
   0x080486ec <+109>:	cmp    eax,DWORD PTR [ebp-0xc]
```

It's just a check of input length. So the number of loops depends on the number of characters inputted. 
We analyze the loop:
```asm
   0x0804869f <+32>:	mov    edx,DWORD PTR [ebp-0x10]
   0x080486a2 <+35>:	mov    eax,DWORD PTR [ebp+0x8]
   0x080486a5 <+38>:	add    eax,edx
   0x080486a7 <+40>:	movzx  eax,BYTE PTR [eax]
   0x080486aa <+43>:	mov    BYTE PTR [ebp-0x11],al
   0x080486ad <+46>:	movsx  eax,BYTE PTR [ebp-0x11]
   0x080486b1 <+50>:	sub    esp,0xc
   0x080486b4 <+53>:	push   eax
   0x080486b5 <+54>:	call   0x80485d1 <rol4>
   0x080486ba <+59>:	add    esp,0x10
   0x080486bd <+62>:	mov    BYTE PTR [ebp-0x11],al
   0x080486c0 <+65>:	xor    BYTE PTR [ebp-0x11],0x16
   0x080486c4 <+69>:	movsx  eax,BYTE PTR [ebp-0x11]
   0x080486c8 <+73>:	sub    esp,0xc
   0x080486cb <+76>:	push   eax
   0x080486cc <+77>:	call   0x80485f8 <ror8>
   0x080486d1 <+82>:	add    esp,0x10
   0x080486d4 <+85>:	mov    BYTE PTR [ebp-0x11],al
   0x080486d7 <+88>:	mov    edx,DWORD PTR [ebp-0x10]
   0x080486da <+91>:	mov    eax,DWORD PTR [ebp+0x8]
   0x080486dd <+94>:	add    edx,eax
   0x080486df <+96>:	movzx  eax,BYTE PTR [ebp-0x11]
   0x080486e3 <+100>:	mov    BYTE PTR [edx],al
   0x080486e5 <+102>:	add    DWORD PTR [ebp-0x10],0x1
```
   
In brief:

  - ebp - 0x10: counter of the loop.
   
  - ebp + 0x8: our input(is passed as an argument in encrypt())
    
In the first loop offset(counter) is zero and movzx sends to eax the first byte of input_data.
Then this byte goes through a left rotation of 4 bits. The result is XORed with 0x16. Then we have a right rotation of 8 bits.
We notice that last procedure(ror8) does not affect the final outcome. More or less that's how an input is encrypted.

> # rol4()

When rotating left(4 bits), 4 bits are shifted to the left. The 4 most significant bits come bach in on the right.
Here, rotation takes place to a byte, so the 4 most significant  bits that go outside the byte on the left come back in on the right.

For example: Let's take 0x70:

0 1 1 1   0 0 0 0 : 0x70

0 0 0 0   0 1 1 1 : 0x7

The same thing happens with ror8().

Now, we have everything we need to crack this program:

Reversing assembly code to pseudo code we get something like this: (Remember we want to decrypt those hex values we got)
```
for (i = 0; i < length_of_user_input; i++) {
        data = rol8(ciphertext)
        data ^= 0x16
        result = rol4(data)
        print result
}
```
Okay, let's build two scripts, one in C, and one in python.
Remember A xor B = C --> A = B xor C and rol4 is reversed to ror4 (likewise, ror8 becomes rol8). See [here](https://www.aldeid.com/wiki/Category:Encryption/rol-ror)

```C
#include <stdio.h>
#include <string.h>

#define INT_BITS 8
#define ROl 8
#define ROR 4
int leftRotate(int n, unsigned int d)
{
    return (n << d) | (n >> (INT_BITS - d));
}

int rightRotate(int n, unsigned int d)
{
    return (n >> d) | (n << (INT_BITS - d));
}

int eightbits(int number)
{
    return (((1 << INT_BITS) - 1) & number);
}

int main ()
{

    char hex[] = "118020E0225372A101415520A0C025E33540659575003085C1";
    int i = 0;
    char data[] = "00";
    while (i < strlen(hex)) {
        data[0] = hex[i];
        data[1] = hex[i+1];
        int val = (int) strtol(data, NULL, 16);  // convert string to int with base 16
        int n = eightbits(leftRotate(val, 8));  // leftRotate 8 bits and keep only the 8 least signifacant bits. This part could be skipped 
        n ^= 22;  //xor with 0x16 (22 decimal)
        printf("%c", eightbits(rightRotate(n, ROL)));
        i += 2;
    }
    putchar('\n');
    return 0;
}

```

```python

INT_BITS = 8
ROR = 4
def rightRotate(n, d):
    return (n >> d) | (n << (INT_BITS - d))

def keep8bits(number):
    return (((1 << 8) - 1) & number)


encrypted = "118020E0225372A101415520A0C025E33540659575003085C1"
i = 0
for i in range(0, len(encrypted), 2):
    n = (int(encrypted[i] + encrypted[i+1], 16) ^ 22)
    print(chr(keep8bits(rightRotate(n, ROR))), end = '')

```

As I said before, rol8 is useless so we can skip it.

   
  
   
   

