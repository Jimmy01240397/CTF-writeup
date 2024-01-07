#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include "SECCOMP.h"

struct sock_filter seccompfilter[]={
	BPF_STMT(BPF_LD | BPF_W | BPF_ABS, ArchField),
	BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0),
	BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
	BPF_STMT(BPF_LD | BPF_W | BPF_ABS, SyscallNum),
	Allow(open),
	Allow(openat),
	Allow(read),
	Allow(write),
	Allow(close),
	Allow(readlink),
	Allow(getdents),
	Allow(getrandom),
	Allow(brk),
	Allow(rt_sigreturn),
	Allow(exit),
	Allow(exit_group),
	BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
};

struct sock_fprog filterprog={
	.len=sizeof(seccompfilter)/sizeof(struct sock_filter),
	.filter=seccompfilter
};

void apply_seccomp(){
	if(prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0)){
		perror("Seccomp Error");
		exit(1);
	}
	if(prctl(PR_SET_SECCOMP,SECCOMP_MODE_FILTER,&filterprog)==-1){
		perror("Seccomp Error");
		exit(1);
	}
	return;
}

void jackpot()
{
	puts("Here is your flag");
	printf("%s\n", "flag{fake}");
}

int main(void)
{
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	apply_seccomp();
	char name[100];
	unsigned long ticket_pool[0x10];
	int number;
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	puts("Lottery!!");
	printf("Give me your number: ");
	scanf("%d", &number);
	printf("Here is your ticket 0x%lx\n", ticket_pool[number]);
	printf("Sign your name: ");
	read(0, name, 0x100);
	if (ticket_pool[number] == jackpot)
	{
		puts("You get the jackpot!!");
		jackpot();
	}
	else
		puts("You get nothing QQ");
	return 0;
}
