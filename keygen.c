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

	if (c > 57)
		c -= 55;
	else 
		c -= 48;

	return  c;

}

bool check(char sol[], int o)
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

void permute(char  a[], int l, int r)  
{  
    // Base case  
    if (l == r) {
		if (check(a, r+1)){
			for (int i = 0; i <= r; i++)
				printf("%c", a[i]);
			printf("\n");
		}
	}

    else
    {  
        // Permutations made  
        for (int i = l; i <= r; i++)  
        {  
  
            // Swapping done  
            swap(&a[l], &a[i]);  
  
            // Recursion called  
            permute(a, l+1, r);  
  
            //backtrack  
            swap(&a[l], &a[i]);  
        }  
    }  
}  
  

char * combinations(char poss_data[], char sol[], int start, int end, int index, int k)
{
	if (index == k) {
		permute(sol,0, 15);
		return sol;
	}
	
	for (int i = start; i <= end && end - i + 1 >= k - index; i++) {
		sol[index] = poss_data[i];
		combinations(poss_data, sol, i + 1, end, index + 1, k);
	}
}


int main ()
{
	char poss[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9','A', 'B', 'C', 'D','E','F','G', '@', '/'};//,'H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'};
	char sol[16];
	combinations(poss, sol, 0, 18, 0, 16); 

		
	return 0;
}

	

