# Write-up for be-quick-or-be-dead-3 challenge
# PicoCTF_2018: be-quick-or-be-dead-3

**Category:** Reversing
**Points:** 350

> As the [song](https://www.youtube.com/watch?v=CTt1vk9nM9c) draws closer to the end, another executable **be-quick-or-be-dead-3** suddenly pops up. 
This one requires even faster machines. Can you run it fast enough too? 

Let's run the binary:

```console
user@user:~/ ./be-quick-or-be-dead-3

Be Quick Or Be Dead 3
=====================

Calculating key...
You need a faster machine. Bye bye.
```

Time to analyze the binary with gdb.

```asm
Dump of assembler code for function main:
   0x00000000004008a6 <+0>:	push   rbp
   0x00000000004008a7 <+1>:	mov    rbp,rsp
   0x00000000004008aa <+4>:	sub    rsp,0x10
   0x00000000004008ae <+8>:	mov    DWORD PTR [rbp-0x4],edi
   0x00000000004008b1 <+11>:	mov    QWORD PTR [rbp-0x10],rsi
   0x00000000004008b5 <+15>:	mov    eax,0x0
   0x00000000004008ba <+20>:	call   0x400868 <header>
   0x00000000004008bf <+25>:	mov    eax,0x0
   0x00000000004008c4 <+30>:	call   0x4007c1 <set_timer>
   0x00000000004008c9 <+35>:	mov    eax,0x0
   0x00000000004008ce <+40>:	call   0x400815 <get_key>
   0x00000000004008d3 <+45>:	mov    eax,0x0
   0x00000000004008d8 <+50>:	call   0x400840 <print_flag>
   0x00000000004008dd <+55>:	mov    eax,0x0
   0x00000000004008e2 <+60>:	leave  
   0x00000000004008e3 <+61>:	ret    
End of assembler dump.
```

The `main` function is similar to the previous two challenges.
Just like last time, if we disable the timer, we hang and the program does not return in a reasonable time.

Again, the `get_key` function calls the `calculate_key` function which is the interesting part.

```asm
Dump of assembler code for function get_key:
   0x0000000000400815 <+0>:	push   rbp
   0x0000000000400816 <+1>:	mov    rbp,rsp
   0x0000000000400819 <+4>:	mov    edi,0x400a08
   0x000000000040081e <+9>:	call   0x400530 <puts@plt>
   0x0000000000400823 <+14>:	mov    eax,0x0
   0x0000000000400828 <+19>:	call   0x400792 <calculate_key>
   0x000000000040082d <+24>:	mov    DWORD PTR [rip+0x20087d],eax        # 0x6010b0 <key>
   0x0000000000400833 <+30>:	mov    edi,0x400a1b
   0x0000000000400838 <+35>:	call   0x400530 <puts@plt>
   0x000000000040083d <+40>:	nop
   0x000000000040083e <+41>:	pop    rbp
   0x000000000040083f <+42>:	ret    
End of assembler dump.
```

> Calculate_Key()

```asm
Dump of assembler code for function calculate_key:
   0x0000000000400792 <+0>:	push   rbp
   0x0000000000400793 <+1>:	mov    rbp,rsp
   0x0000000000400796 <+4>:	mov    edi,0x19965
   0x000000000040079b <+9>:	call   0x400706 <calc>
   0x00000000004007a0 <+14>:	pop    rbp
   0x00000000004007a1 <+15>:	ret    
End of assembler dump.
```

This time `calculate_key()` calls `calc()` with 0x19965 as a parameter. Let's see what is hiding there.
```asm
Dump of assembler code for function calc:
   0x0000000000400706 <+0>:	push   rbp
   0x0000000000400707 <+1>:	mov    rbp,rsp
   0x000000000040070a <+4>:	push   r12
   0x000000000040070c <+6>:	push   rbx
   0x000000000040070d <+7>:	sub    rsp,0x20
   0x0000000000400711 <+11>:	mov    DWORD PTR [rbp-0x24],edi
   0x0000000000400714 <+14>:	cmp    DWORD PTR [rbp-0x24],0x4
   0x0000000000400718 <+18>:	ja     0x40072b <calc+37>
   0x000000000040071a <+20>:	mov    eax,DWORD PTR [rbp-0x24]
   0x000000000040071d <+23>:	imul   eax,DWORD PTR [rbp-0x24]
   0x0000000000400721 <+27>:	add    eax,0x2345
   0x0000000000400726 <+32>:	mov    DWORD PTR [rbp-0x14],eax
   0x0000000000400729 <+35>:	jmp    0x400786 <calc+128>
   0x000000000040072b <+37>:	mov    eax,DWORD PTR [rbp-0x24]
   0x000000000040072e <+40>:	sub    eax,0x1
   0x0000000000400731 <+43>:	mov    edi,eax
   0x0000000000400733 <+45>:	call   0x400706 <calc>
   0x0000000000400738 <+50>:	mov    ebx,eax
   0x000000000040073a <+52>:	mov    eax,DWORD PTR [rbp-0x24]
   0x000000000040073d <+55>:	sub    eax,0x2
   0x0000000000400740 <+58>:	mov    edi,eax
   0x0000000000400742 <+60>:	call   0x400706 <calc>
   0x0000000000400747 <+65>:	sub    ebx,eax
   0x0000000000400749 <+67>:	mov    eax,DWORD PTR [rbp-0x24]
   0x000000000040074c <+70>:	sub    eax,0x3
   0x000000000040074f <+73>:	mov    edi,eax
   0x0000000000400751 <+75>:	call   0x400706 <calc>
   0x0000000000400756 <+80>:	mov    r12d,eax
   0x0000000000400759 <+83>:	mov    eax,DWORD PTR [rbp-0x24]
   0x000000000040075c <+86>:	sub    eax,0x4
   0x000000000040075f <+89>:	mov    edi,eax
   0x0000000000400761 <+91>:	call   0x400706 <calc>
   0x0000000000400766 <+96>:	sub    r12d,eax
   0x0000000000400769 <+99>:	mov    eax,r12d
   0x000000000040076c <+102>:	add    ebx,eax
   0x000000000040076e <+104>:	mov    eax,DWORD PTR [rbp-0x24]
   0x0000000000400771 <+107>:	sub    eax,0x5
   0x0000000000400774 <+110>:	mov    edi,eax
   0x0000000000400776 <+112>:	call   0x400706 <calc>
   0x000000000040077b <+117>:	imul   eax,eax,0x1234
   0x0000000000400781 <+123>:	add    eax,ebx
   0x0000000000400783 <+125>:	mov    DWORD PTR [rbp-0x14],eax
   0x0000000000400786 <+128>:	mov    eax,DWORD PTR [rbp-0x14]
   0x0000000000400789 <+131>:	add    rsp,0x20
   0x000000000040078d <+135>:	pop    rbx
   0x000000000040078e <+136>:	pop    r12
   0x0000000000400790 <+138>:	pop    rbp
   0x0000000000400791 <+139>:	ret    
End of assembler dump.
```

Okay, it's neither too big nor too small.
We see a lot of recursions. 
It's better to break code into smaller pieces. 

```asm
0x0000000000400711 <+11>:	mov    DWORD PTR [rbp-0x24],edi
0x0000000000400714 <+14>:	cmp    DWORD PTR [rbp-0x24],0x4
 ```
Argument is stored into memory and it is compared with 4.
If arg <= 4: 

```asm
0x000000000040071a <+20>:	mov    eax,DWORD PTR [rbp-0x24]
0x000000000040071d <+23>:	imul   eax,DWORD PTR [rbp-0x24]
0x0000000000400721 <+27>:	add    eax,0x2345
0x0000000000400726 <+32>:	mov    DWORD PTR [rbp-0x14],eax
0x0000000000400729 <+35>:	jmp    0x400786 <calc+128>
```

We move arg to eax, we multiply it by itself and we add to the result 0x2345.

> arg = arg*arg + 0x2345


Now, if arg > 4:

> # First recursive call:

```asm
   0x000000000040072b <+37>:	mov    eax,DWORD PTR [rbp-0x24]
   0x000000000040072e <+40>:	sub    eax,0x1
   0x0000000000400731 <+43>:	mov    edi,eax
   0x0000000000400733 <+45>:	call   0x400706 <calc>
```

We just call `calc` with **arg - 1**.

> # Second recursive call:

```asm
   0x0000000000400738 <+50>:	mov    ebx,eax
   0x000000000040073a <+52>:	mov    eax,DWORD PTR [rbp-0x24]
   0x000000000040073d <+55>:	sub    eax,0x2
   0x0000000000400740 <+58>:	mov    edi,eax
   0x0000000000400742 <+60>:	call   0x400706 <calc>
```

We store result of first recursion into ebx and then we call `calc` with **arg - 2**.

> # Third recursive call:

```asm
 0x0000000000400747 <+65>:	sub    ebx,eax
 0x0000000000400749 <+67>:	mov    eax,DWORD PTR [rbp-0x24]
 0x000000000040074c <+70>:	sub    eax,0x3
 0x000000000040074f <+73>:	mov    edi,eax
 0x0000000000400751 <+75>:	call   0x400706 <calc>
```
We subtract from calc(arg - 1) the result of calc(arg - 2)
and then we call `calc(arg - 3)` .

> # Fourth recursive call:

```asm
   0x0000000000400756 <+80>:	mov    r12d,eax
   0x0000000000400759 <+83>:	mov    eax,DWORD PTR [rbp-0x24]
   0x000000000040075c <+86>:	sub    eax,0x4
   0x000000000040075f <+89>:	mov    edi,eax
   0x0000000000400761 <+91>:	call   0x400706 <calc>
```
Result of previous recursion is saved into r12d and then program calls `calc(arg - 4)` .

> # Fifth recursive call:

```asm
   0x0000000000400766 <+96>:	sub    r12d,eax
   0x0000000000400769 <+99>:	mov    eax,r12d
   0x000000000040076c <+102>:	add    ebx,eax
   0x000000000040076e <+104>:	mov    eax,DWORD PTR [rbp-0x24]
   0x0000000000400771 <+107>:	sub    eax,0x5
   0x0000000000400774 <+110>:	mov    edi,eax
   0x0000000000400776 <+112>:	call   0x400706 <calc>
   0x000000000040077b <+117>:	imul   eax,eax,0x1234
   0x0000000000400781 <+123>:	add    eax,ebx
   0x0000000000400783 <+125>:	mov    DWORD PTR [rbp-0x14],eax
   0x0000000000400786 <+128>:	mov    eax,DWORD PTR [rbp-0x14]
```

Similarly, we subtract from calc(arg - 4) result of calc(arg - 3). 

Τhe results of the two subtractions are added and stored to ebx.

`calc(arg - 5)` is called. The result is multiplied with 0x1234 and is added to the value of ebx.

Recursion is too slow as you may already know. Why?
Because, we calculate the same  values (call function with the same parameter) too many times.

Say hello to dynamic programming. [recursion](https://www.geeksforgeeks.org/recursion/) and [dynamic programming](https://www.geeksforgeeks.org/dynamic-programming/).

Dynamic Programming is mainly an optimization over plain recursion. 
Wherever we see a recursive solution that has repeated calls for same inputs, 
we can optimize it using Dynamic Programming. The idea is to simply store the results of subproblems, 
so that we do not have to re-compute them when needed later (That's the main problem of recursion as I said above).

To calculate the key we're gonna use bottom-up DP.

```C
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#define N 104806
int main ()
{
    uint32_t dp[N]; // Note that we use uint32_t in order to simulate the overflows that occur 
                    // when adding 32-bit integers (as in the original assembly).
    memset(dp, 0, N*sizeof(dp[0]));
    
    // These are the first four base states when arg <= 4.
    dp[0] = 9029; 
    dp[1] = 9030;
    dp[2] = 9033;
    dp[3] = 9038;
    dp[4] = 9045;
    
    // With those values we compute the other ones.
    for (int i = 5; i < N; i++)
        dp[i] = (((dp[i - 1] - dp[i - 2]) + (dp[i - 3] - dp[i - 4])) + dp[i-5]*4660); // we analyzed it before.

    printf("%u\n", dp[N - 1]); // we print the unsigned value (it doesn't really matter) 
    return 0;
}
```
The result is stoed in eax.

```bash
gcc -o recursion recursion.c
```


```console
user@user:~/ ./recursion

2653079950
```

Now, we know exactly what to do so I skip the other parts of the solution and I go straight to the script.
```bash
cp -p be-quick-or-be-dead-3 be-quick-or-be-dead-3_patched
rasm2 'mov eax, 2653079950' | xxd -p -r | dd conv=notrunc of=be-quick-or-be-dead-3_patched bs=1 seek=$((0x828)) 2>/dev/null
./be-quick-or-be-dead-3_patched | tail -1
```
Congratulations!!!



