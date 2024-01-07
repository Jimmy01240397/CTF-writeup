#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/mman.h>
#include <string.h>
#include <fcntl.h>
#define MAX_STATE 0x100
#define EVAL_TIMES 0x100

void init()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
}

typedef struct Trans_{
    int alphabet;
    unsigned int next_state;
} Trans;

typedef struct State_{
    unsigned int stateid;
    uint16_t off;
    size_t trans_num;
    Trans* trans;
} State;

State* DFA;
size_t DFA_State_num;
int (*DFA_func)(char *input, char *end);

void input_DFA()
{
    size_t state_num;
    printf("How many state? (max: %u) ", MAX_STATE);
    scanf("%lu", &state_num);
    if(state_num>MAX_STATE){
        puts("Too many state.");
        exit(0);
    }
    DFA_State_num = state_num;
    DFA = (State*)malloc(sizeof(State)*DFA_State_num);
    for(unsigned int i=0;i<DFA_State_num;i++){
        printf("How many transitions for state %u? (max: 128) ", i);
        unsigned int trans_num=0;
        scanf("%u", &trans_num);
        if(trans_num>128){
            puts("Too many transitions.");
            exit(0);
        }
        DFA[i].stateid=i;
        DFA[i].trans_num=trans_num;
        DFA[i].trans = (Trans*)calloc(1, sizeof(Trans)*trans_num);
        for(int j=0;j<trans_num;j++){
            printf("Transition %d:\nAlphabet (input ASCII code 0~127): ", j);
            int alphabet=0;
            scanf("%d", &alphabet);
            if(alphabet>127){
                puts("Invalid ascii code.");
                exit(0);
            }
            for(int k=0;k<j;k++){
                if(DFA[i].trans[k].alphabet == alphabet){
                    puts("Alphabet duplicated.");
                    exit(0);
                }
            }
            DFA[i].trans[j].alphabet = alphabet;
            unsigned int next_state=0;
            printf("Next state: ");
            scanf("%u", &next_state);
            if(next_state>=DFA_State_num){
                puts("Invalid state id.");
                exit(0);
            }
            DFA[i].trans[j].next_state=next_state;
        }
    }
}

size_t build_DFA()
{
    size_t bytecode_sz=0;
    for(int i=0;i<DFA_State_num;i++){
        DFA[i].off = (uint16_t)bytecode_sz;
        bytecode_sz += 9;
        bytecode_sz += DFA[i].trans_num * 12;
        bytecode_sz += 5;
    }
    uint16_t Accept_State = (uint16_t)bytecode_sz+9;
    uint16_t Reject_State = (uint16_t)bytecode_sz+9+8;
    if(bytecode_sz > 0x10000){
        puts("DFA too large.");
        exit(0);
    }
    size_t memsz = (((bytecode_sz)>>12)+1)<<12;
    //printf("Memory Sz: %lu\n", memsz);
    void* bytecode_mem = mmap(0, memsz, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, 0, 0);
    if(bytecode_mem==MAP_FAILED){
        perror("Memory allocation failed");
        exit(0);
    }
    DFA_func = bytecode_mem;
    //size_t bytecode_
    void *Accept_addr = bytecode_mem;
    for(int i=0;i<DFA_State_num;i++){
        void *state_base = (void*)((size_t)bytecode_mem + DFA[i].off);
        if(i==DFA_State_num-1){
            memcpy(state_base, "\x48\x39\xf7\x0f\x84", 5); //cmp rdi, rsi; je ...
            int accept_state_off = (int)(int16_t)(Accept_State - (DFA[i].off+9));
            memcpy((void*)((size_t)state_base+5), &accept_state_off, 4);
            state_base = (void*)((size_t)state_base + 9);
        }
        memcpy(state_base, "\x48\x31\xc0\x8a\x07\x48\x83\xc7\x01", 9); //xor rax,rax;mov  al, BYTE PTR [rdi]; add    rdi, 0x1;
        state_base = (void*)((size_t)state_base + 9);
        for(int j=0;j<DFA[i].trans_num;j++){
            void *trans_base = (void*)((size_t)state_base + (size_t)j*12);
            uint16_t trans_off;
            if(i==DFA_State_num-1){
                trans_off = (uint16_t)(DFA[i].off+9+9+(uint16_t)j*12);
            }
            else{
                trans_off = (uint16_t)(DFA[i].off+9+(uint16_t)j*12);
            }
            memcpy(trans_base, "\x48\x3d", 2); // cmp
            memcpy((void*)((size_t)trans_base+2), &DFA[i].trans[j].alphabet, 4);
            int next_state_off = (int)(int16_t)(DFA[DFA[i].trans[j].next_state].off-(trans_off+12));
            memcpy((void*)((size_t)trans_base+6), "\x0f\x84", 2); // je
            memcpy((void*)((size_t)trans_base+8), &next_state_off, 4);
        }
        void *state_default_trans = (void*)((size_t)state_base + (size_t)DFA[i].trans_num*12);
        uint16_t state_default_trans_off = (uint16_t)(DFA[i].off+9+(uint16_t)DFA[i].trans_num*12);
        if(i==DFA_State_num-1){
            state_default_trans_off += 9;
        }
        memcpy(state_default_trans, "\xe9", 1); // jmp
        int reject_state_off = (int)(int16_t)(Reject_State - (state_default_trans_off+5));
        memcpy((void*)((size_t)state_default_trans+1), &reject_state_off, 4);
        Accept_addr = (void*)((size_t)Accept_addr + (9+5+12*(size_t)DFA[i].trans_num));
        if(i==DFA_State_num-1){
            Accept_addr = (void*)((size_t)Accept_addr + 9);
        }
    }
    void *Reject_addr = (void*)((size_t)Accept_addr + 8);
    memcpy(Accept_addr, "\x48\xc7\xc0\x01\x00\x00\x00\xc3", 8); //mov    rax, 0x1;ret
    memcpy(Reject_addr, "\x48\xc7\xc0\x00\x00\x00\x00\xc3", 8); //mov    rax, 0x0;ret
    mprotect(DFA_func, memsz, PROT_READ|PROT_EXEC);
    return bytecode_sz;
}

void debug_bytecode(size_t bytecode_sz)
{
    puts("Output the bytecode to file.");
    int fd = open("dfacode.mem", O_CREAT|O_RDWR, S_IRWXU);
    char *ptr = (char*)DFA_func;
    size_t remain_sz = bytecode_sz;
    while(remain_sz){
        size_t writesz = write(fd, ptr, remain_sz);
        remain_sz -= writesz;
    }
    close(fd);
}

int main()
{
    init();
    input_DFA();
    size_t bytecode_length = build_DFA();
    //debug_bytecode(bytecode_length);
    printf("DFA has been built!");
    char buf[256];
    memset(buf,0,sizeof(buf));
    for(int i=0;i<EVAL_TIMES;i++){
        printf("EVAL> ");
        scanf("%255s",buf);
        if(buf){
            int res = DFA_func(buf, &buf[strlen(buf)]);
            if(res){
                printf("Accept\n");
            }
            else{
                printf("Reject\n");
            }
        }
    }
    return 0;
}