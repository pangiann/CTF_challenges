// DANGER: VERY SLOPPY - BAD CODE.
// Please Wear Appropriate Eye Protection.

/*
 ===================================================
 Name         : keygen-me-1
 Author       : WhiteRose13 aka Panagiotis Giannoulis 
 Version      : 1.0
 Description  : KeyGenerator in C
 ===================================================

*/

// Finds all permutations of 26 uppercase letters and 9 numbers 
// and checks if they are valid, considering the assembly code of
// --activate-- 


#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#define VALID 36
#define LENGTH 16
void swap(char *xp, char *yp)
{
    char temp = *xp;
    *xp = *yp;
    *yp = temp;
}

int ord(int c)
{

	// 9's ascii value is 57
	// 7's ascii value is 55
	// 0's ascii value is 48
	if (c > 57)
		return c - 55;
	return c - 48;

}


// The tricky part about validate_key is to notice that this function actually operates a modulo with 36. 
// If we use gdb we'll see that multiplying by 0x38e38e39h and right shifting 3 bits results in division by 36.
bool validate_key(char sol[])
{
	int i = 0;
	int x = 0;
	for (i = 0; i < LENGTH - 1; i++)
		x += (ord((int) sol[i]) + 1) * (i + 1);
		

//	Below we see what assembly is doing
/*
	long long  y = 954437177;
	unsigned long long  z = x * y;
	z = z >> 32;
	z = z >> 3;
	int k = z << 3;
	k += z;
	k = k << 2;
	x -= k;
	
*/
	//As mentioned above, we found out that the whole operation is a modulo with 36
	x %= 36;
	int res = ord(sol[LENGTH - 1]);
	if (x == res)
		return true;
	return false;
}

void permute_with_repetition(char  sol[], char arr[], int index, int k)  
{  
	for (int i = 0; i < k; i++) {
		sol[index] = arr[i];

		if (index == k - 1) {
			if( validate_key(sol))
					printf("%s\n", sol);
		}
		else
			permute_with_repetition(sol, arr, index + 1, k);


	}  
}  
  

char * combinations(char poss_data[], char arr[], int start, int end, int index, int k)
{
	if (index == k) {
		char sol[LENGTH];
		permute_with_repetition(sol, arr, 0, LENGTH);
		return arr;
	}
	
	for (int i = start; i < end && end - i  >= k - index; i++) {
		arr[index] = poss_data[i];
		combinations(poss_data, arr, i + 1, end, index + 1, k);
	}
}


int main ()
{
	//func_validation_key is ignored
	//Accepts only a key with uppercase letters of English alphabet or numbers 0 - 9

	//first we need to choose from 36 only 16 possible characters
	//then we need to find all permutations with repetition of them.
	char poss[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	char sol[LENGTH];
	combinations(poss, sol, 0, VALID, 0, LENGTH); 

		
	return 0;
}

	

