# PicoCTF_2018: Key_gen_2

**Category:** Reversing 
**Points:** 750
>The software has been updated. Can you find us a new product key for the program in /problems/keygen-me-2_3_5e45e804e9c1a9de2f8124266b173c35

# Prerequisites:
  - Good knowledge of assembly language
  - gdb 
  - C programming language
 
  

# Hints:
  - First use gdb to disassemble the program
  - Try to understand what main and other functions(check_valid_key, validate_key etc.) do
  - Then try to convert assembly code to C - language
  - Last but not least, create a script in whatever language you want to generate all valid keys
 
# Solution:
Very similar to keygen-me-1. Again valid input is a string of 16 characters(digit or uppercase).

The difference here is that in validate_key() there are 12 constraints(functions):

  - key_constraintXX()
  
If all of them return true we have found the right key.

Example of a key_constraint func:

>    key_constraint01(char sol[]) 
>
>    {
>
>        return (ord(sol[0]) + ord(sol[1]))%36 == 14
>
>    }
> 

## keygen2:

Download the files and then just run:

>./keygen2

Close the program with Ctrl-c(or wait it to finish) and pick a valid key.
Then run:

> ./activate [valid key]

Congrats! The flag will appear in your terminal.
