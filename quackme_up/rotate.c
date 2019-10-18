#include <stdio.h>
#include <string.h>

#define INT_BITS 8
#define ROL 4
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
		int val = (int) strtol(data, NULL, 16);
		int n = val ^ 22;
		printf("%c", eightbits(leftRotate(n, ROL)));
		i += 2;
	}
	putchar('\n');
	return 0;
}


