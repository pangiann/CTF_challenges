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




int mod(int x)
{
	return  x % 36;

}


bool key_con1(char s1, char s2)
{
	if (mod(ord(s1) + ord(s2)) == 14)
		return true;
	return false;
}

bool key_con2(char s1, char s2)
{
	if (mod(ord(s1) + ord(s2)) == 24)
		return true;
	return false;
}

bool key_con3(char s1, char s2)
{
	if (mod(ord(s1) - ord(s2)) == 6)
		return true;
	return false;
}

bool key_con4(char s1, char s2, char s3)
{
	if (mod(ord(s1) + ord(s2) + ord(s3)) == 4)
		return true;
	return false;
}
bool key_con5(char s1, char s2, char s3)
{
	if (mod(ord(s1) + ord(s2) + ord(s3)) == 13)
		return true;
	return false;
}
bool key_con6(char s1, char s2, char s3)
{
	if (mod(ord(s1) + ord(s2) + ord(s3)) == 22)
		return true;
	return false;
}

bool key_con7(char s1, char s2, char s3)
{
	if (mod(ord(s1) + ord(s2) + ord(s3)) == 31)
		return true;
	return false;
}
bool key_con8(char s1, char s2, char s3)
{
	if (mod(ord(s1) + ord(s2) + ord(s3)) == 7)
		return true;
	return false;
}

bool key_con9(char s1, char s2, char s3)
{
	if (mod(ord(s1) + ord(s2) + ord(s3)) == 20)
		return true;
	return false;
}

bool key_con10(char s1, char s2, char s3)
{
	if (mod(ord(s1) + ord(s2) + ord(s3)) == 12)
		return true;
	return false;
}
bool key_con11(char s1, char s2, char s3)
{
	if (mod(ord(s1) + ord(s2) + ord(s3)) == 27)
		return true;
	return false;
}
bool key_con12(char s1, char s2, char s3)
{
	if (mod(ord(s1) + ord(s2) + ord(s3)) == 23)
		return true;
	return false;
}
int brute_force(char arr[], int valid)
{

	int counter = 0;
	char sol[] = "0000000000000000";
	for (int i = 0; i < valid; i++) {
		for (int j = 0; j < valid; j++) { 
			if (key_con1(arr[i], arr[j])) {
				sol[0] = arr[i];
				sol[1] = arr[j];
				for (int i = 0; i < valid; i++) {
					for (int j = 0; j < valid; j++) {
						if (key_con2(arr[i], arr[j])) {
							sol[2] = arr[i];
							sol[3] = arr[j];
							if (key_con3(sol[2], sol[0])) {
								for (int i = 0; i < valid; i++) {
									if (key_con4(sol[1], sol[3], arr[i])) {
										sol[5] = arr[i];
										for (int i = 0; i < valid; i++) {
											for (int j = 0; j < valid; j++) {
												if (key_con5(sol[2], arr[i], arr[j])) {
													sol[4] = arr[i];
													sol[6] = arr[j];
													if (key_con6(sol[3], sol[4], sol[5])) {
														for (int i = 0; i < valid; i++) {
															for (int j = 0; j < valid; j++) {
																if (key_con7(sol[6], arr[i], arr[j])) {
																	sol[8] = arr[i];
																	sol[10] = arr[j];
																	for (int i = 0; i < valid; i++) {
																		if (key_con8(sol[1], sol[4], arr[i])) {
																			sol[7] = arr[i];
																			for (int i = 0; i < valid; i++) {
																				for (int j = 0; j < valid; j++) {
																					for (int k = 0; k < valid; k++) {
																						if (key_con9(arr[i], arr[j], arr[k])) {
																							sol[9] = arr[i];
																							sol[12] = arr[j];
																							sol[15] = arr[k];
																							for (int i = 0; i < valid; i++) {
																								for (int j = 0; j < valid; j++) {
																									if (key_con10(arr[i], arr[j], sol[15])) {
																										sol[13] = arr[i];
																										sol[14] = arr[j];
																										if (key_con11(sol[8], sol[9], sol[10])) 
																											if (key_con12(sol[7], sol[12], sol[13])) {
																												sol[16] = '\0';
																												printf("%s\n", sol);
																												counter++;
																											}
																										else continue;
																									}
																									else continue;
																								}
																							}
																						}
																						else continue;
																					}
																				}
																			}
																		}
																		else continue;
																	}
																}
																else continue;
															}
														}
													}
													else continue;
												}
												else continue;
											}
										}
									}
									else continue;
								}
							}
							else continue;
						}		
						else continue;
					}			
				}
			}
			else continue;
		}
	}
	return counter;
}

																														






int main ()
{
	//func_validation_key is ignored
	//Accepts only a key with uppercase letters of English alphabet or numbers 0 - 9

	char poss[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"; 
	printf("all possible keys are: %d\n", brute_force(poss, 36));


		
	return 0;
}

	

