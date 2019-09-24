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
  
## keygen1:

Download the files and then just run:

>./keygen 

Close the program with Ctrl-c and pick a valid key.
Then run:

> ./activate [valid key]

Congrats! The flag will appear in your terminal.
