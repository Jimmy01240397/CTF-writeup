#ifndef _INSN_EMULATOR_H_
#define _INSN_EMULATOR_H_
#define RAM_SIZE 0x8000

#include <stdint.h>

typedef enum {
    STORE,
    COPY,
} UsbComm_t;

struct dev_t {
    char opaque[0x100];
    uint16_t port;
    void (*in_handler)(void*,void*,uint16_t);
    void (*out_handler)(void*,void*,uint16_t);
};

struct vcpu_t {
    uint64_t r1;
    uint64_t r2;
    uint64_t r3;
    uint64_t r4;
    uint64_t r5;
    uint64_t rsp;
    uint64_t rbp;
    uint64_t rip;
    uint64_t phys_off;
    struct dev_t *dev;
};

typedef enum {
    NOP,
    ADD,
    SUB,
    MUL,
    SHL,
    SHR,
    MOV,
    RET,
    CALL,
    SYC,
    IN,
    OUT,
    OPCODE_CNT,
} Opcode_t;

typedef enum {
    R1,
    R2,
    R3,
    R4,
    R5,
    RSP,
    RBP,
    RIP,
    MEM,
    VAL,
    OP_CNT,
} Op_t;

typedef enum {
    READ,
    WRITE,
    EXIT,
    USB,
} Syc_t;

struct insn_t {
    Opcode_t opcode;
    Op_t op1, op2;
};
extern int (*opcode_jt[OPCODE_CNT])(struct vcpu_t *self, uint64_t *addr1, uint64_t *addr2);

struct vcpu_t *get_new_vm(void *ram);
int run_vm(struct vcpu_t *vcpu);

#endif /* _INSN_EMULATOR_H_ */