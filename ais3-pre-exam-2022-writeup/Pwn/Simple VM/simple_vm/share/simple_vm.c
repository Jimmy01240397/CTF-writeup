#include "simple_vm.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define op_get_addr(_op)  (((uint64_t) _op) & ~((1 << 4) - 1))
#define virt_to_phys(addr, vcpu) ((uint64_t) addr + vcpu->phys_off)
#define phys_to_virt(addr, vcpu) ((uint64_t) addr - vcpu->phys_off)

// ========== USB ==========
void usb_in_handler(void *_dev, void *param, uint16_t comm)
{
    struct dev_t *dev = (struct dev_t *) _dev;
    switch (comm) {
    case STORE: memcpy(dev->opaque, param, 0x100);
    }
}

void usb_out_handler(void *_dev, void *param, uint16_t comm)
{
    struct dev_t *dev = (struct dev_t *) _dev;
    switch (comm) {
    case COPY: memcpy(param, dev->opaque, 0x100);
    }
}

void create_usb(struct vcpu_t *vcpu)
{
    if (vcpu->dev != NULL)
        return;
    
    struct dev_t *usb = malloc(sizeof(struct dev_t));
    memset(usb->opaque, 0, 0x100);
    usb->port = 0x77;
    usb->in_handler = usb_in_handler;
    usb->out_handler = usb_out_handler;
    vcpu->dev = usb;
}
// =========================

int op_nop(struct vcpu_t *self, uint64_t *addr1, uint64_t *addr2) { return 0; }
int op_add(struct vcpu_t *self, uint64_t *addr1, uint64_t *addr2) { *addr1 += *addr2; return 0; }
int op_sub(struct vcpu_t *self, uint64_t *addr1, uint64_t *addr2) { *addr1 -= *addr2; return 0; }
int op_shl(struct vcpu_t *self, uint64_t *addr1, uint64_t *addr2) { *addr1 <<= *addr2; return 0; }
int op_shr(struct vcpu_t *self, uint64_t *addr1, uint64_t *addr2) { *addr1 >>= *addr2; return 0; }
int op_mul(struct vcpu_t *self, uint64_t *addr1, uint64_t *addr2) { *addr1 *= *addr2; return 0; }
int op_mov(struct vcpu_t *self, uint64_t *addr1, uint64_t *addr2) { *addr1 =  *addr2; return 0; }

int op_ret(struct vcpu_t *self, uint64_t *addr1, uint64_t *addr2)
{
    uint64_t *rsp = (uint64_t *) virt_to_phys(self->rsp, self);
    self->rip = *--rsp;
    self->rsp += 8;
    if (self->rsp > self->rbp)
        return -1;
    return 0;
}

int op_call(struct vcpu_t *self, uint64_t *addr1, uint64_t *addr2)
{
    if (self->rsp > self->rbp)
        return -1;

    uint64_t *rsp = (uint64_t *) virt_to_phys(self->rsp, self);
    self->rsp -= 8;
    *rsp-- = self->rip;
    self->rip = *addr1;
    return 0;
}

int op_syn(struct vcpu_t *self, uint64_t *addr1, uint64_t *addr2)
{
    switch (*addr1) {
    case READ:
        if (self->r2 + self->r3 >= RAM_SIZE)
            return -1;
        read(0, (uint64_t *) virt_to_phys(self->r2, self), (self->r3 > 0x100) ? 0x100 : self->r3); break;
    case WRITE:
        if (self->r2 + self->r3 >= RAM_SIZE)
            return -1;
        write(1, (uint64_t *) virt_to_phys(self->r2, self), (self->r3 > 0x100) ? 0x100 : self->r3); break;
    case EXIT:  printf("VM exit normally\n"); exit(0); break;
    case USB:   create_usb(self); break;
    }
    return 0;
}

int op_in(struct vcpu_t *self, uint64_t *addr1, uint64_t *addr2)
{
    if (self->dev == NULL)
        return -1;

    if (self->r5 >= RAM_SIZE)
        return -1;

    void *param = (void *) virt_to_phys(self->r5, self);
    if (*addr1 == self->dev->port)
        self->dev->in_handler(self->dev, param, *addr2);
}

int op_out(struct vcpu_t *self, uint64_t *addr1, uint64_t *addr2)
{
    if (self->dev == NULL)
        return -1;

    if (self->r5 >= RAM_SIZE)
        return -1;
    
    void *param = (void *) virt_to_phys(self->r5, self);
    if (*addr1 == self->dev->port)
        self->dev->out_handler(self->dev, param, *addr2);
}

int (*opcode_jt[OPCODE_CNT])(struct vcpu_t *self, uint64_t *addr1, uint64_t *addr2) = \
{
    op_nop, op_add, op_sub, op_mul, op_shl, op_shr, op_mov,
    op_ret, op_call, op_syn, op_in, op_out,
};

struct vcpu_t *get_new_vm(void *ram)
{
    struct vcpu_t *vcpu = malloc(sizeof(struct vcpu_t));
    vcpu->r1  = 0;
    vcpu->r2  = 0;
    vcpu->r3  = 0;
    vcpu->r4  = 0;
    vcpu->r5  = 0;
    vcpu->rsp = 0;
    vcpu->rbp = 0;
    vcpu->rip = 0;
    vcpu->phys_off = (uint64_t) ram;
    vcpu->dev = NULL;
    return vcpu;
}

static inline void get_insn(struct insn_t *insn, struct vcpu_t *vcpu)
{
    uint16_t *ptr = (uint16_t *) virt_to_phys(vcpu->rip, vcpu);
    insn->opcode = ptr[0];
    insn->op1 = ptr[1];
    insn->op2 = ptr[2];
    vcpu->rip += 6;
}

int run_vm(struct vcpu_t *vcpu)
{
    struct insn_t insn;
    uint64_t *addr1, *addr2;
    uint64_t tmp;

    while (vcpu->rip < RAM_SIZE)
    {
        addr1 = NULL;
        addr2 = NULL;

        get_insn(&insn, vcpu);

        if (insn.opcode >= OPCODE_CNT)
            return -1;

        switch (insn.op1 & 0xf) {
        case R1:  addr1 = &vcpu->r1; break;
        case R2:  addr1 = &vcpu->r2; break;
        case R3:  addr1 = &vcpu->r3; break;
        case R4:  addr1 = &vcpu->r4; break;
        case R5:  addr1 = &vcpu->r5; break;
        case RSP: addr1 = &vcpu->rsp; break;
        case RBP: addr1 = &vcpu->rbp; break;
        case RIP: addr1 = &vcpu->rip; break;
        case MEM:
            if (op_get_addr(insn.op2) >= RAM_SIZE)
                return -1;
            addr1 = (uint64_t *) virt_to_phys(op_get_addr(insn.op1), vcpu); break;
        }

        switch (insn.op2 & 0xf) {
        case R1:  addr2 = &vcpu->r1; break;
        case R2:  addr2 = &vcpu->r2; break;
        case R3:  addr2 = &vcpu->r3; break;
        case R4:  addr2 = &vcpu->r4; break;
        case R5:  addr2 = &vcpu->r5; break;
        case RSP: addr2 = &vcpu->rsp; break;
        case RBP: addr2 = &vcpu->rbp; break;
        case RIP: addr2 = &vcpu->rip; break;
        case VAL: tmp = insn.op2 >> 4; addr2 = &tmp; break;
        case MEM:
            if (op_get_addr(insn.op2) >= RAM_SIZE)
                return -1;
            addr2 = (uint64_t *) virt_to_phys(op_get_addr(insn.op2), vcpu); break;
        }

        if (addr1 == NULL || addr2 == NULL)
            return -1;

        if (opcode_jt[insn.opcode](vcpu, addr1, addr2) == -1)
            return -1;
    }
}

int main()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    char *ram = malloc(RAM_SIZE);
    read(0, ram, RAM_SIZE);
    
    struct vcpu_t *vcpu = get_new_vm(ram);
    
    if (run_vm(vcpu) == -1)
        printf("VM exit accidentally\n");
    else
        printf("VM exit normally\n");
}