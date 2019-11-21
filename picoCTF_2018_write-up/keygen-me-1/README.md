# PicoCTF_2018: Key_gen_1

**Category:** Reversing 
**Points:** 400
>Can you generate a valid product key for the validation program in /problems/keygen-me-1_0_2b06ee615c1b7021f1eff5829aae5006

# Prerequisites:
  - Good knowledge of assembly language
  - gdb 
  - C programming language
  - Python to write key generator(optional but much easier)
  - Algorithms for permutations and combinations

# Hints:
  - First use gdb to disassemble the program
  - Try to understand what main and other functions(check_valid_key, validate_key etc.) do
  - Then try to convert assembly code to c - language
  - Last but not least, create a script in whatever language you want to generate all valid keys
# Solution:
``` check_valid_char() ```
  - Returns true if character is a digit (0 - 9)
  - Returns true if character is an uppercase english letter ('A' - 'Z')

``` check_valid_key() ```
  - Returns true if length of our key is 16 &&
  - && each one of the key's characters pass check_valid_char()
  
``` ord() ```
  - If digit, returns digit as an integer
  - If letter, decreases character's ascii value by 55 and returns the result

``` validate_key() ```
  - Calls ord for every character
  - Sums up the results
  - Operate sum modulo 36
  - Returns true if the result is equal to the ord(16th caracter)

```C
bool validate_key(char sol[])
{
	int i = 0;
	int x = 0;
	for (i = 0; i < LENGTH - 1; i++)
		x += (ord((int) sol[i]) + 1) * (i + 1);
	x %= 36;
	int res = ord(sol[LENGTH - 1]);
	if (x == res)
		return true;
	return false;
}
```
  

## keygen1:

Download the files and then just run:
```bash
> ./keygen 
```
Close the program with Ctrl-c and pick a valid key.
Then run:
```bash
> ./activate [valid key]
```
Congrats! The flag will appear in your terminal.
