#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>

void (*const preinit_array []) (void)
     __attribute__ ((section (".preinit_array"),
                     aligned (sizeof (void *)))) =
{
    0x401f00,
};

int main(int argc, char *argv[])
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    char buf[0x10] = {0};
    puts("The read@plt and write@plt are little weird ...");
    puts("Has any code done before main function ? 🤔");

    while (1)
    {
        printf("read or write (r/w)\n> ");
        read(0, buf, 2);
        
        switch (buf[0]) {
        case 'r': read(0, buf+2, 0xe); break;
        case 'w': write(1, buf+2, 0xe); break;
        default: return 0;
        }
    }
}