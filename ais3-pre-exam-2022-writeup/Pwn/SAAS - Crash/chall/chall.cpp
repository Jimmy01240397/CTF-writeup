#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

class String {
   public:
	char *str;
	size_t len;

	String(const char *s) {
		len = strlen(s);
		str = new char[len + 1];
		strcpy(str, s);
	}
	~String() { delete[] str; }
};

const int MAX_STRS = 16;
char tmp[4096];
String *strs[MAX_STRS] = {};

int readidx() {
	char c;
	int idx;
	printf("Index: ");
	scanf("%d%c", &idx, &c);
	if (idx < 0 || idx >= MAX_STRS) {
		printf("Bad index\n");
		exit(0);
	}
	return idx;
}

void print(String s) {
	printf("Length: %zu\n", s.len);
	printf("Content: ");
	write(1, s.str, s.len);
	printf("\n");
}

void menu() {
	printf("===== S(tring)AAS =====\n");
	printf("1. Create string\n");
	printf("2. Edit string\n");
	printf("3. Print string\n");
	printf("4. Delete string\n");
}

int main() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	while (true) {
		int choice, idx;
		char c;
		menu();
		printf("> ");
		scanf("%d", &choice);
		switch (choice) {
			case 1:
				idx = readidx();
				printf("Content: ");
				scanf("%4095[^\n]", tmp);
				scanf("%c", &c);
				strs[idx] = new String(tmp);
				break;
			case 2:
				idx = readidx();
				printf("New Content: ");
				if (strs[idx] != nullptr) {
					scanf("%4095[^\n]", tmp);
					scanf("%c", &c);
					memcpy(strs[idx]->str, tmp, strs[idx]->len);
					strs[idx]->str[strs[idx]->len] = 0;
				} else {
					printf("String #%d doesn't exist!\n", idx);
				}
				break;
			case 3:
				idx = readidx();
				if (strs[idx] != nullptr) {
					print(*strs[idx]);
				} else {
					printf("String #%d doesn't exist!\n", idx);
				}
				break;
			case 4:
				idx = readidx();
				if (strs[idx] != nullptr) {
					delete strs[idx];
					strs[idx] = nullptr;
				} else {
					printf("String #%d doesn't exist!\n", idx);
				}
				break;
			default:
				puts("Bad option");
				exit(0);
		}
	}
	return 0;
}
