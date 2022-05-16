#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdint.h>
#include <signal.h>
#include <string.h>

#define KEYS_SIZE 4

uint8_t curr_key_idx = 0;
uint64_t keys[ KEYS_SIZE ];

int main();

void perror(const char *msg)
{
    printf("ERROR: %s\n", msg);
    exit(1);
}

static inline void gen_key()
{
    int fd = open("/dev/random", O_RDONLY);
    if (fd == -1)
        perror("open /dev/random failed");
    
    for (int i = 0; i < KEYS_SIZE; i++)
        read(fd, &keys[i], 2);
    
    close(fd);
}

#define ret_addr      ((uint64_t)__builtin_return_address(0))
#define ret_addr_addr ((uint64_t)__builtin_frame_address(0) + 8)
#define enc_addr(addr, key) ((key << 48) | addr)
#define dec_addr(addr, key) ((key << 48) ^ addr)

#define sign()   do { (*(uint64_t *)ret_addr_addr) = \
                                  enc_addr(ret_addr, keys[curr_key_idx++]); } while (0)
#define unsign() do { (*(uint64_t *)ret_addr_addr) = \
                                  dec_addr(ret_addr, keys[--curr_key_idx]); } while (0)
#define check()  do { const char _c = *(char *)ret_addr; } while (0)
#define unsign_and_check() { unsign(); check(); }

int getint(int64_t *ret)
{
    sign();

    char buf[0x10] = {0};
    read(0, buf, 0x100);
    
    int64_t val = strtol(buf, NULL, 10);
    if (val == 0) {
        unsign_and_check();
        return -1;
    }

    *ret = val;
    unsign_and_check();
    return 0;
}

void restore(int signo)
{
    puts("One more chance ...");
    main();
}

#define operation_function(_op, _operator)                     \
    void _op(int64_t *a, int64_t *b)                           \
    {                                                          \
        sign();                                                \
        printf("a: ");                                         \
        getint(a);                                             \
        printf("b: ");                                         \
        getint(b);                                             \
        printf("a " #_operator " b = %ld\n", *a _operator *b); \
        unsign_and_check();                                    \
    }

operation_function(add, +);
operation_function(sub, -);
operation_function(mul, *);

void sum(int64_t *a, int64_t *b)
{
    sign();

    int64_t sum = 0;
    *a = 0, *b = 0;

    puts("[ADD]");
    add(a, b); sum += *a + *b;
    puts("[SUB]");
    sub(a, b); sum += *a - *b;
    puts("[MUL]");
    mul(a, b); sum += *a * *b;
    printf("sum = %ld\n", sum);
    
    unsign_and_check();
}

int main()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    gen_key();
    signal(SIGSEGV, restore);
    sign();

    int64_t opt, a, b;
    while (1)
    {
        printf("Super Calculator\n"
               "1. add\n"
               "2. sub\n"
               "3. mul\n"
               "4. sum\n"
               "5. bye\n> ");
        switch (getint(&opt)) {
        case -1: exit(1);
        case 0:
            switch (opt) {
            case 1: add(&a, &b); break;
            case 2: sub(&a, &b); break;
            case 3: mul(&a, &b); break;
            case 4: sum(&a, &b); break;
            case 5: goto main_bye;
            }
        }
    }

main_bye:
    unsign_and_check();
    return 0;
}