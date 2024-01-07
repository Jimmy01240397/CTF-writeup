#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

struct Student
{
	char uuid[0x20];
	char name[0x200];
	char id[0x100];
	int used;
};

#define STU_SZ 0x10
struct Student students[STU_SZ];

char *CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
void *randstr(char *dst, int len)
{
	srand(time(0));
	for (int i = 0; i < len; ++i)
		dst[i] = CHARSET[rand() % 62];
	dst[len - 1] = 0;
}

void response_regist(char *uuid)
{
	char *key;
	char *val;
	char buf[0x400];
	bzero(buf, 0x400);
	
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "{");

	key = "\"uuid\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", key);
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", ": ");
	val = "\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", val);
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", uuid);
	val = "\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", val);
	key = "%s";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), key, ",");

	key = "\"status\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", key);
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", ": ");
	val = "\"register success\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", val);
	key = "%s";

	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "}");

	puts(buf);
}

struct QQ
{
	char buf[0x400];
	char *str[8];
};

void response_regist_error(char *name, char *id)
{
	char *str[8];
	
	str[0] = "%d";
	str[1] = "%s";
	str[2] = "%s";
	str[3] = "{";
	str[4] = "}";
	str[5] = ": ";
	str[6] = ",";
	str[7] = "\"";

	char *key;
	char *val;

	char *buf = alloca(0x400);
	bzero(buf, 0x400);

	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[3]);

	key = "\"name\"";
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[2], key);
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[1], str[5]);
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[1], str[7]);
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[1], name);
	val = "\"";
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[2], val);
	key = "%s";
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, key, str[6]);

	key = "\"id\"";
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[2], key);
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[1], str[5]);
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[1], str[7]);
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[1], id);
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[1], str[7]);
	key = "%s";
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, key, str[6]);

	key = "\"msg\"";
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[2], key);
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[1], str[5]);
	val = "\"";
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[2], val);
	val = "The EDU-CTF course is currently at full capacity, and we are unable to accept more students at the moment. If any students drop the course, you can still apply for enrollment. You are welcome to make multiple attempts. If you're unable to secure a spot, you are encouraged to try again next semester. ";
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[2], val);
	val = "So sorry, ";
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[2], val);
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[1], name);
	strcat(buf, ".");
	val = "\"";
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[2], val);
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[1], str[6]);

	key = "\"status\"";
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[2], key);
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[1], str[5]);
	val = "\"register fail\"";
	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[2], val);
	key = "%s";


	__sprintf_chk(&buf[strlen(buf)], 1, 0x400, str[4]);

	puts(buf);
}

void regist(char *name, char *id)
{
	int idx = 0;
	for (; idx < STU_SZ; ++idx)
		if (!students[idx].used) break;

	if (idx == STU_SZ)
	{
		response_regist_error(name, id);
		exit(-1);
	}
	
	randstr(students[idx].uuid, sizeof(students[idx].uuid));
	strcpy(students[idx].name, name);
	strcpy(students[idx].id, id);
	students[idx].used = 1;

	response_regist(students[idx].uuid);
}

void response_notfound()
{
	char *key;
	char *val;
	char buf[0x300];
	
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "{");
	key = "\"status\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", key);
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", ": ");
	val = "\"not found\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", val);
	key = "%s";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "}");
	__printf_chk(1, buf);
}

void response_search_found(char *name, char *id)
{
	char *key;
	char *val;
	char buf[0x400];
	bzero(buf, 0x400);
	
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "{");
	key = "\"name\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", key);
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", ": ");
	val = "\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", val);
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", name);
	val = "\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", val);
	key = "%s";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), key, ",");
	
	key = "\"id\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", key);
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", ": ");
	val = "\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", val);
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", id);
	val = "\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", val);
	key = "%s";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), key, ",");

	key = "\"status\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", key);
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", ": ");
	val = "\"found\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", val);
	key = "%s";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "}");
	puts(buf);
}

void search(char *uuid)
{
	int idx = 0;
	for (; idx < STU_SZ; ++idx)
		if (strcmp(uuid, students[idx].uuid) == 0) break;
	if (idx == STU_SZ)
		response_notfound();
	else
		response_search_found(students[idx].name, students[idx].id);
}

void response_cancel(char *name, char *id)
{
	char *key;
	char *val;
	char buf[0x400];
	bzero(buf, 0x400);
	
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "{");
	key = "\"name\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", key);
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", ": ");
	val = "\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", val);
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", name);
	val = "\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", val);
	key = "%s";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), key, ",");
	
	key = "\"id\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", key);
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", ": ");
	val = "\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", val);
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", id);
	val = "\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", val);
	key = "%s";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), key, ",");

	key = "\"status\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", key);
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", ": ");
	val = "\"cancel\"";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "%s", val);
	key = "%s";
	__sprintf_chk(&buf[strlen(buf)], 1, sizeof(buf), "}");
	puts(buf);
}

void cancel(char *uuid)
{
	int idx = 0;
	for (; idx < STU_SZ; ++idx)
		if (strcmp(uuid, students[idx].uuid) == 0) break;
	if (idx == STU_SZ)
		response_notfound();
	else
	{
		response_cancel(students[idx].name, students[idx].id);
		memset(students[idx].uuid, 0, sizeof(students[idx].uuid));
		memset(students[idx].name, 0, sizeof(students[idx].name));
		memset(students[idx].id, 0, sizeof(students[idx].id));
		students[idx].used = 0;
	}
}

void menu()
{
    puts("+==========    Registration    ==========+");
    puts("| 1. Register                            |");
    puts("| 2. Search                              |");
    puts("| 3. Cancel                              |");
    puts("+========================================+");
    printf("> ");
}

int main(void)
{
	setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
	
	char name[0x200];
	char id[0x100];
	char uuid[0x20];
	int choice;

	for (;;)
	{
		menu();
		scanf("%d", &choice);
		getchar();

		switch(choice)
		{
		case 1:
			printf("Name: ");
			fgets(name, 0x200, stdin);
			printf("ID: ");
			fgets(id, 0x100, stdin);
			regist(name, id);
			break;
		case 2:
			printf("UUID: ");
			fgets(uuid, 0x20, stdin);
			search(uuid);
			break;
		case 3:
			printf("UUID: ");
			read(0, uuid, 0x20);
			cancel(uuid);
			break;
		default:
			printf("Invalid choice.\n");
			exit(-1);
		}
	}

	return 0;
}
