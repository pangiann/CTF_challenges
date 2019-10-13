# Write-up for quackme challenge
# PicoCTF_2018: quackme

**Category:** Reversing
**Points:** 200

>Can you deal with the Duck Web? Get us the flag from this program. 
You can also find the program in /problems/quackme_2_45804bbb593f90c3b4cefabe60c1c4e2.

In reversing problems, we are trying to understand what exactly assembly code does and convert it in a pseudocode. We use a disassembler like gdb or radare.
Then, we create a script to generate the reversed result. 
Let's disassemble main function:
```asm
/ (fcn) main 87
|   int main (int argc, char **argv, char **envp);
|           ; var int32_t var_4h @ ebp-0x4
|           ; arg int32_t arg_4h @ esp+0x4
|           ; DATA XREF from entry0 @ 0x80484f7
|           0x08048715      8d4c2404       lea ecx, [arg_4h]
|           0x08048719      83e4f0         and esp, 0xfffffff0
|           0x0804871c      ff71fc         push dword [ecx - 4]
|           0x0804871f      55             push ebp
|           0x08048720      89e5           mov ebp, esp
|           0x08048722      51             push ecx
|           0x08048723      83ec04         sub esp, 4
|           0x08048726      a144a00408     mov eax, dword [obj.stdout] ; obj.stdout__GLIBC_2.0
|                                                                      ; [0x804a044:4]=0
|           0x0804872b      6a00           push 0                      ; size_t size
|           0x0804872d      6a02           push 2                      ; 2 ; int mode
|           0x0804872f      6a00           push 0                      ; char *buf
|           0x08048731      50             push eax                    ; FILE*stream
|           0x08048732      e879fdffff     call sym.imp.setvbuf        ; int setvbuf(FILE*stream, char *buf, int mode, size_t size)
|           0x08048737      83c410         add esp, 0x10
|           0x0804873a      83ec0c         sub esp, 0xc
|           0x0804873d      68f0870408     push str.You_have_now_entered_the_Duck_Web__and_you_re_in_for_a_honkin__good_time.__Can_you_figure_out_my_trick ; 0x80487f0 ; "You have now entered the Duck Web, and you're in for a honkin' good time.\nCan you figure out my trick?" ; const char *s
|           0x08048742      e829fdffff     call sym.imp.puts           ; int puts(const char *s)
|           0x08048747      83c410         add esp, 0x10
|           0x0804874a      e8f3feffff     call sym.do_magic
|           0x0804874f      83ec0c         sub esp, 0xc
|           0x08048752      68bb880408     push str.That_s_all_folks.  ; 0x80488bb ; "That's all folks." ; const char *s
|           0x08048757      e814fdffff     call sym.imp.puts           ; int puts(const char *s)
|           0x0804875c      83c410         add esp, 0x10
|           0x0804875f      b800000000     mov eax, 0
|           0x08048764      8b4dfc         mov ecx, dword [var_4h]
|           0x08048767      c9             leave
|           0x08048768      8d61fc         lea esp, [ecx - 4]
\           0x0804876b      c3             ret
```

do_magic function seems to be the one we're intrested for.
```asm

/ (fcn) sym.do_magic 211
|   sym.do_magic ();
|           ; var uint32_t var_1dh @ ebp-0x1d
|           ; var uint32_t var_1ch @ ebp-0x1c
|           ; var int32_t var_18h @ ebp-0x18
|           ; var char *s @ ebp-0x14
|           ; var size_t size @ ebp-0x10
|           ; var void *var_ch @ ebp-0xc
|           ; CALL XREF from main @ 0x804874a
|           0x08048642      55             push ebp
|           0x08048643      89e5           mov ebp, esp
|           0x08048645      83ec28         sub esp, 0x28
|           0x08048648      e88effffff     call sym.read_input
|           0x0804864d      8945ec         mov dword [s], eax
|           0x08048650      83ec0c         sub esp, 0xc
|           0x08048653      ff75ec         push dword [s]              ; const char *s
|           0x08048656      e835feffff     call sym.imp.strlen         ; size_t strlen(const char *s)
|           0x0804865b      83c410         add esp, 0x10
|           0x0804865e      8945f0         mov dword [size], eax
|           0x08048661      8b45f0         mov eax, dword [size]
|           0x08048664      83c001         add eax, 1
|           0x08048667      83ec0c         sub esp, 0xc
|           0x0804866a      50             push eax                    ; size_t size
|           0x0804866b      e8f0fdffff     call sym.imp.malloc         ;  void *malloc(size_t size)
|           0x08048670      83c410         add esp, 0x10
|           0x08048673      8945f4         mov dword [var_ch], eax
|           0x08048676      837df400       cmp dword [var_ch], 0
|       ,=< 0x0804867a      751a           jne 0x8048696
|       |   0x0804867c      83ec0c         sub esp, 0xc
|       |   0x0804867f      6884880408     push str.malloc___returned_NULL._Out_of_Memory ; 0x8048884 ; "malloc() returned NULL. Out of Memory\n" ; const char *s
|       |   0x08048684      e8e7fdffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048689      83c410         add esp, 0x10
|       |   0x0804868c      83ec0c         sub esp, 0xc
|       |   0x0804868f      6aff           push 0xffffffffffffffff     ; int status
|       |   0x08048691      e8eafdffff     call sym.imp.exit           ; void exit(int status)
|       |   ; CODE XREF from sym.do_magic @ 0x804867a
|       `-> 0x08048696      8b45f0         mov eax, dword [size]
|           0x08048699      83c001         add eax, 1
|           0x0804869c      83ec04         sub esp, 4
|           0x0804869f      50             push eax                    ; size_t n
|           0x080486a0      6a00           push 0                      ; int c
|           0x080486a2      ff75f4         push dword [var_ch]         ; void *s
|           0x080486a5      e816feffff     call sym.imp.memset         ; void *memset(void *s, int c, size_t n)
|           0x080486aa      83c410         add esp, 0x10
|           0x080486ad      c745e4000000.  mov dword [var_1ch], 0
|           0x080486b4      c745e8000000.  mov dword [var_18h], 0
|       ,=< 0x080486bb      eb4e           jmp 0x804870b
|       |   ; CODE XREF from sym.do_magic @ 0x8048711
|      .--> 0x080486bd      8b45e8         mov eax, dword [var_18h]
|      :|   0x080486c0      0558880408     add eax, obj.sekrutBuffer   ; 0x8048858 ; ")\x06\x16O+50\x1eQ\x1b[\x14K\b]+VGWP\x16MQQ]"
|      :|   0x080486c5      0fb608         movzx ecx, byte [eax]
|      :|   0x080486c8      8b55e8         mov edx, dword [var_18h]
|      :|   0x080486cb      8b45ec         mov eax, dword [s]
|      :|   0x080486ce      01d0           add eax, edx
|      :|   0x080486d0      0fb600         movzx eax, byte [eax]
|      :|   0x080486d3      31c8           xor eax, ecx
|      :|   0x080486d5      8845e3         mov byte [var_1dh], al
|      :|   0x080486d8      8b1538a00408   mov edx, dword [obj.greetingMessage] ; [0x804a038:4]=0x80487f0 str.You_have_now_entered_the_Duck_Web__and_you_re_in_for_a_honkin__good_time.__Can_you_figure_out_my_trick
|      :|   0x080486de      8b45e8         mov eax, dword [var_18h]
|      :|   0x080486e1      01d0           add eax, edx
|      :|   0x080486e3      0fb600         movzx eax, byte [eax]
|      :|   0x080486e6      3a45e3         cmp al, byte [var_1dh]
|     ,===< 0x080486e9      7504           jne 0x80486ef
|     |:|   0x080486eb      8345e401       add dword [var_1ch], 1
|     |:|   ; CODE XREF from sym.do_magic @ 0x80486e9
|     `---> 0x080486ef      837de419       cmp dword [var_1ch], 0x19
|     ,===< 0x080486f3      7512           jne 0x8048707
|     |:|   0x080486f5      83ec0c         sub esp, 0xc
|     |:|   0x080486f8      68ab880408     push str.You_are_winner     ; 0x80488ab ; "You are winner!" ; const char *s
|     |:|   0x080486fd      e86efdffff     call sym.imp.puts           ; int puts(const char *s)
|     |:|   0x08048702      83c410         add esp, 0x10
|    ,====< 0x08048705      eb0c           jmp 0x8048713
|    ||:|   ; CODE XREF from sym.do_magic @ 0x80486f3
|    |`---> 0x08048707      8345e801       add dword [var_18h], 1
|    | :|   ; CODE XREF from sym.do_magic @ 0x80486bb
|    | :`-> 0x0804870b      8b45e8         mov eax, dword [var_18h]
|    | :    0x0804870e      3b45f0         cmp eax, dword [size]
|    | `==< 0x08048711      7caa           jl 0x80486bd
|    |      ; CODE XREF from sym.do_magic @ 0x8048705
|    `----> 0x08048713      c9             leave
\           0x08048714      c3             ret
```

Okay, the eye goes straight to this instruction: **0x080486f8      68ab880408     push str.You_are_winner     ; 0x80488ab ; "You are winner!" ; const char *s **

How can we go there in order to win? 
var_1ch which is ebp - 0x1c (a value in the stack) is compared to 0x19 (decimal 25).
```asm
 0x080486ef      837de419       cmp dword [var_1ch], 0x19
 ```
 Hmm, above that we can see that there is an instruction that adds 1 to ebp - 0x1c.
 ```asm
 0x080486eb      8345e401       add dword [var_1ch], 1
 ```
 Ofcourse this is happening if we pass a test. Here is the magic think. We need to pass 25 tests. We notice a loop. At the bottom of the assembly we can find
 condition checking.
 ```asm
 0x0804870e      3b45f0         cmp eax, dword [size]
 0x08048711      7caa           jl 0x80486bd
```
Debugging the program, we can see that this is a check of input length.  So the number of loops depends on the number of characters inputted.
So, first thing we find is that we need to input 25 characters.
But, what characters?

We analyze the loop:
```asm
; CODE XREF from sym.do_magic @ 0x8048711
0x080486bd      8b45e8         mov eax, dword [var_18h]
0x080486c0      0558880408     add eax, obj.sekrutBuffer   ; 0x8048858 ; ")\x06\x16O+50\x1eQ\x1b[\x14K\b]+VGWP\x16MQQ]"
0x080486c5      0fb608         movzx ecx, byte [eax]
0x080486c8      8b55e8         mov edx, dword [var_18h]
0x080486cb      8b45ec         mov eax, dword [s]
0x080486ce      01d0           add eax, edx
0x080486d0      0fb600         movzx eax, byte [eax]
0x080486d3      31c8           xor eax, ecx
0x080486d5      8845e3         mov byte [var_1dh], al
0x080486d8      8b1538a00408   mov edx, dword [obj.greetingMessage] ; [0x804a038:4]=0x80487f0 str.You_have_now_entered_the_Duck_Web__and_you_re_in_for_a_honkin__good_time.__Can_you_figure_out_my_trick
0x080486de      8b45e8         mov eax, dword [var_18h]
0x080486e1      01d0           add eax, edx
0x080486e3      0fb600         movzx eax, byte [eax]
0x080486e6      3a45e3         cmp al, byte [var_1dh]
0x080486e9      7504           jne 0x80486ef
0x080486eb      8345e401       add dword [var_1ch], 1
```
Okay, in brief:
var_18h is the counter of the loop.

sekrutBuffer is some binary data, some hex values.

[s] is the address of our input.

So, the first time offset(counter) is zero and movzx movs in ecx the first byte of the binary_data and in eax the first byte of our input.

Then the most crucial instruction happens:
```ams
0x080486d3      31c8           xor eax, ecx
```
We xor those two values and finally we  compare the result with the first byte of string: You have now entered the Duck Web, and you're in for a honkin' good time.
\nCan you figure out my trick? 
If the result of xor is equal with the first byte of string we increment  ebp - 0x1c. 
Second time we xor 2nd byte of binary_data with input_data and compare the result with the 2nd byte of the above string.
This procedure happens 25 times( it should happen 25 times, and it should succeed 25 times).

Reversing assembly code to pseudo code we get something like this:
```
res = 0
for (i = 0; i < length_of_user_input; i++) {
	data = user_input[i] xor binary_data[i]
	if (data == message[i]) {
		res++;
	}
	if (res == 25) {
		print "You are winner!"
	}
}
```
Let's leak the values of the binary data.
```asm
[0x080484e0]> px @ obj.sekrutBuffer
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x08048858  2906 164f 2b35 301e 511b 5b14 4b08 5d2b  )..O+50.Q.[.K.]+
0x08048868  5647 5750 164d 5151 5d00 4e6f 206c 696e  VGWP.MQQ].No lin
```
We get the first 25 bytes.

Okay, let's build two scripts, one in C, and one in python.
Remember A xor B = C --> A = B xor C, so we can generate our input.

```C
#include <stdio.h>
int main ()
{

    char binary_data[] = "2906164f2b35301e511b5b144b085d2b56475750164d51515d";
    char message[] = "You have now entered the Duck Web, and you're in for a honkin' good time.";


    char flag[] = "";

    char data[] = "00";

    for (int i = 0, j = 0; i < strlen(binary_data) - 1; i+=2, j++) {

        //taking first two numbers of binary(one byte)
        data[0] = binary_data[i];
        data[1] = binary_data[i+1];
        
        int val = (int) strtol(data, NULL, 16); (convert string to decimal integer with base 16)
        /* in first loop we have string 29 and we convert it to integer 41. */


        // xor val with decimal (Ascii) value of message.
        int temp = ((int) message[j]) ^ val;


        // print the result
        printf("%c", temp);
        
    }
    putchar('\n');
    return 0;
}
```

This will give us  the flag.

Script in python:
```python
sekrutBuffer = "2906164f2b35301e511b5b144b085d2b56475750164d51515d"

message = "You have now entered the Duck Web, and you're in for a honkin' good time.\nCan you figure out my trick?"

flag = ''
j = 0
for i in range(0, len(sekrutBuffer), 2):

    # int() converts string to decimal integer with base 16
    # ord() converts character to (decimal) ascii value
    # chr() converts decimal integer to character (using ascii table)
    flag += chr(int(sekrutBuffer[i] +  sekrutBuffer[i+1], 16) ^ ord(message[j]))
    j += 1

print flag

```


```bash
python quackme.py | ./main
```

 


