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
		c -= 55;
	else 
		c -= 48;

	return  c;

}


// validate_key function is just doing what assembly code of activate raw file did. 
// Until now, I don't understand the meaning of those things.
// However, it produces the right keys.
bool validate_key(char sol[], int o)
{
	int i = 0;
	unsigned long long x = 0;
	int m = 0;
	while (i < o) {


		x += m;
		m = ord((int) sol[i]);


		m++;
		i++;
		m *= i;
	}

	long long  y = 954437177;
	unsigned long long  z = x * y;
	z = z >> 32;
	z = z >> 3;
	int k = z << 3;
	k += z;
	k = k << 2;
	x -= k;
	int res = ord(sol[15]);
	if (x == res)
		return true;
	return false;
}

void permute_with_repetition(char  sol[], char arr[], int index, int k)  
{  
	for (int i = 0; i <= k; i++) {
		sol[index] = arr[i];

		if (index == k) {
			if( validate_key(sol, k + 1))
					printf("%s\n", sol);
		}
		else
			permute_with_repetition(sol, arr, index + 1, k);


	}  
}  
  

char * combinations(char poss_data[], char arr[], int start, int end, int index, int k)
{
	if (index == k) {
		char sol[16];
		permute_with_repetition(sol, arr, 0, 15);
		return arr;
	}
	
	for (int i = start; i <= end && end - i + 1 >= k - index; i++) {
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
	char poss[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9','A', 'B', 'C', 'D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'};
	char sol[16];
	combinations(poss, sol, 0, 35, 0, 16); 

		
	return 0;
}

	

