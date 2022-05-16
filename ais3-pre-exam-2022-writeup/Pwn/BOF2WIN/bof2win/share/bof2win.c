#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <fcntl.h>

void get_the_flag()
{
    char buf[0x30] = {0};
    int fd = open("/home/bof2win/flag", O_RDONLY);
    read(fd, buf, 0x30);
    write(1, buf, 0x30);
    close(fd);
}

int main()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    char buf[0x10];
    
    puts("What's your name?");
    gets(buf);
    
    printf("Hello, %s!\n", buf);
    return 0;
}
