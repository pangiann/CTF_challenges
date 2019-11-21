#include <stdio.h>
#include <stdint.h>
int main ()
{
	int n = 1067;
	uint32_t first = 0;
	uint32_t second = 1;
	for (int i = 1; i < n; i++) {
		uint32_t temp = second;
		second += first;
		first = temp;
	}

	printf("%d\n", second);
	return 0;
}
		

