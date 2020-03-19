#include <stdio.h>




int book[MAX];
int count = 0;

void make_note()
{
	if (count > 20) {
		printf("limit reached\n");
		return;
	}
	else {
		printf("size of note: \n");
		rbp_C = read_int32();


		rbp_8 = malloc(0x28);
		if (rbp_8 + 0x20 == 0) {
			addr = malloc(rbp_C);
			rbp_8 + 0x20 = addr;
		}

		else {
			printf("title\n");
			read(0, rbp_8, 0x20);
			printf("note\n");
			read(0, rbp_8 + 0x20, rbp_C - 1);
			
			book[count] = rbp_8
			count++;
		}
	}
}

int get_note()
{
	printf("Note#: \n");
	int rbp_4 = read_int32();
	if(rbp_4 < 0 || rbp_4 > count) {
		puts("invalid\n");
		return 0;
	}
	else {
		addr = book[count];
		return addr;
	}

}


void edit_note()
{
	rbp_8 = get_note();
	if (rbp_8 == 0) return;
	
	printf("Title %s: ", rbp_8);
	
	int size = strlen(rbp_8 + 0x20);

	read(0, rbp_8 + 0x20, size);

}

void delete_note() 
{
	rbp_8 = get_note();
	if (rbp_8 == 0) return;

	
	//first freeing 
	free(rbp_8 + 0x20);
	count--;
	book[count] = 0;
}

void print_note()
{
	rbp_8 = get_note();
	if (rbp_8 == 0) return;

    printf("%s : %s\n", rbp_8 rbp_8 + 0x20);
}










			






