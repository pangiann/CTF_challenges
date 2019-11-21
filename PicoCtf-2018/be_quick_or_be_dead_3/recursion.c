#include <stdio.h>
#include <string.h>
#include <stdint.h>
#define N 104806
int main ()
{
	uint32_t dp[N];
	memset(dp, 0, N*sizeof(dp[0]));
	dp[0] = 9029;
	dp[1] = 9030;
	dp[2] = 9033;
	dp[3] = 9038;
	dp[4] = 9045;
	for (int i = 5; i < N; i++) 
		dp[i] = (((dp[i - 1] - dp[i - 2]) + (dp[i - 3] - dp[i - 4])) + dp[i-5]*4660);
	
	printf("%u\n", dp[N - 1]);
	return 0;
}
