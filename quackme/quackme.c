#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int hexadecimalToDecimal(char hexVal[])
{
    int len = strlen(hexVal);

	//printf("len = %d\n", len);
    // Initializing base value to 1, i.e 16^0
    int base = 1;

    int dec_val = 0;

    // Extracting characters as digits from last character
    for (int i = len - 1; i >= 0; i--)
    {
        // if character lies in '0'-'9', converting
        // it to integral 0-9 by subtracting 48 from
        // ASCII value.
        if (hexVal[i] >= '0' && hexVal[i] <= '9')
        {
            dec_val += (hexVal[i] - 48)*base;

            // incrementing base by power
            base *= 16;
        }

        // if character lies in 'A'-'F' , converting
        // it to integral 10 - 15 by subtracting 55
        // from ASCII value
        else if (hexVal[i] >= 'a' && hexVal[i] <= 'f')
        {
            dec_val += (hexVal[i] - 87)*base;

            // incrementing base by power
            base *= 16;
        }
    }

    return dec_val;
}
int main ()
{
	
	char xorData[] = "2906164f2b35301e511b5b144b085d2b56475750164d51515d";
	char message[] = "You have now entered the Duck Web, and you're in for a honkin' good time.";


	char flag[] = "";

	char data[] = "00";

	for (int i = 0, j = 0; i < strlen(xorData) - 1; i+=2, j++) {
		
		data[0] = xorData[i];
		data[1] = xorData[i+1];
		//int val = hexadecimalToDecimal(data);


		int val = (int) strtol(data, NULL, 16);
		//printf("hex = %x\n", val);
		

		int temp = ((int) message[j]) ^ val;


		printf("%c", temp);
		//printf("%x\n", temp);



	}
	putchar('\n');
	return 0;
}
			

