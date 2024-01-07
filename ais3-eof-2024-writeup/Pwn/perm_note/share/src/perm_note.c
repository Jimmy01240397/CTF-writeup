#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define NOTE_RDONLY		(1)
#define NOTE_RDWR		(2)

#define NOTE_NUM		(0x8)
#define SZ_LIMIT		(0xc0)

struct note_t
{
	int perm;
	int len;
	char *content;
};

struct note_t *notes[NOTE_NUM];

void read_note()
{
	int page = 0;

	printf("Which page? ");
	scanf("%d", &page);
	if (page >= NOTE_NUM || page < 0)
	{
		printf("Only 8 pages >:(\n");
		exit(-1);
	}
	if (!notes[page])
	{
		printf("This page is empty >:(\n");
		exit(-1);
	}
	printf("Content: \n");
	write(STDOUT_FILENO, notes[page]->content, notes[page]->len);
}

void write_rdonly_note()
{
	int page = 0;
	int size = 0;

	printf("Which page? ");
	scanf("%d", &page);
	if (page >= NOTE_NUM || page < 0)
	{
		printf("Only 8 pages >:(\n");
		exit(-1);
	}
	if (notes[page])
	{
		printf("This page is writed >:(\n");
		exit(-1);
	}
	
	printf("Size? ");
	scanf("%d", &size);
	if (size >= SZ_LIMIT || size < 0)
	{
		printf("Bad size >:(\n");
		exit(-1);
	}
	notes[page] = malloc(sizeof(struct note_t));
	if (!notes[page])
	{
		printf("Malloc note error QQ\n");
		exit(-1);
	}
	notes[page]->content = malloc(size);
	if (!notes[page]->content)
	{
		printf("Malloc content error QQQQ\n");
		exit(-1);
	}
	printf("Content: \n");
	read(STDIN_FILENO, notes[page]->content, size);
	notes[page]->len = strlen(notes[page]->content);
	notes[page]->perm = NOTE_RDONLY;
}

void write_rdwr_note()
{
	int page = 0;
	int size = 0;

	printf("Which page? ");
	scanf("%d", &page);
	if (page >= NOTE_NUM || page < 0)
	{
		printf("Only 8 pages >:(\n");
		exit(-1);
	}
	if (notes[page])
	{
		printf("This page is writed >:(\n");
		exit(-1);
	}
	
	printf("Size? ");
	scanf("%d", &size);
	getchar();
	if (size >= SZ_LIMIT || size < 0)
	{
		printf("Bad size >:(\n");
		exit(-1);
	}
	notes[page] = malloc(sizeof(struct note_t));
	if (!notes[page])
	{
		printf("Malloc note error QQ\n");
		exit(-1);
	}
	notes[page]->content = malloc(size);
	if (!notes[page]->content)
	{
		printf("Malloc content error QQQQ\n");
		exit(-1);
	}
	printf("Content: \n");
	fgets(notes[page]->content, size, stdin);
	notes[page]->len = strlen(notes[page]->content);
	notes[page]->perm = NOTE_RDWR;
}

void rewrite_rdwr_note()
{
	int page = 0;

	printf("Which page? ");
	scanf("%d", &page);
	getchar();
	if (page >= NOTE_NUM || page < 0)
	{
		printf("Only 8 pages >:(\n");
		exit(-1);
	}
	if (!notes[page])
	{
		printf("This page is empty >:(\n");
		exit(-1);
	}

	if (notes[page]->perm == NOTE_RDONLY)
	{
		printf("Read Write Note Only :(\n");
		exit(-1);
	}
	
	printf("Content: \n");
	fgets(notes[page]->content, strlen(notes[page]->content), stdin);
	notes[page]->len = strlen(notes[page]->content);
}

void merge_rdonly_note()
{
	int page_dst = 0;
	int page_src = 0;

	printf("Which page for dest? ");
	scanf("%d", &page_dst);
	if (page_dst >= NOTE_NUM || page_dst < 0)
	{
		printf("Only 8 pages >:(\n");
		exit(-1);
	}
	if (!notes[page_dst])
	{
		printf("This page is empty >:(\n");
		exit(-1);
	}
	
	printf("Which page for src? ");
	scanf("%d", &page_src);
	if (page_src >= NOTE_NUM || page_src < 0)
	{
		printf("Only 8 pages >:(\n");
		exit(-1);
	}
	if (!notes[page_src])
	{
		printf("This page is empty >:(\n");
		exit(-1);
	}

	if (notes[page_dst]->perm == NOTE_RDWR && notes[page_src]->perm == NOTE_RDWR)
	{
		printf("Read Only Note Only :(\n");
		exit(-1);
	}

	notes[page_dst]->content = realloc(notes[page_dst]->content, notes[page_dst]->len + notes[page_src]->len);
	memcpy(&notes[page_dst]->content[notes[page_dst]->len], notes[page_src]->content, notes[page_src]->len);
	notes[page_dst]->len = notes[page_dst]->len + notes[page_src]->len;
	free(notes[page_src]->content);
	notes[page_src]->content = NULL;
	free(notes[page_src]);
	notes[page_src] = NULL;
	printf("Merge done!\n");
}

void delete_note()
{
	int page = 0;

	printf("Which page? ");
	scanf("%d", &page);
	if (page >= NOTE_NUM || page < 0)
	{
		printf("Only 8 pages >:(\n");
		exit(-1);
	}
	if (!notes[page])
	{
		printf("This page is empty >:(\n");
		exit(-1);
	}
	free(notes[page]->content);
	notes[page]->content = NULL;
	free(notes[page]);
	notes[page] = NULL;
	printf("Delete done!\n");
}
void menu()
{
    puts("+==========    Registration    ==========+");
    puts("| 1. Read Note                           |");
    puts("| 2. Wrtie RDONLY Note                   |");
    puts("| 3. Write RDWR Note                     |");
    puts("| 4. Rewrite RDWR Note                   |");
    puts("| 5. Merge RDONLY Note                   |");
    puts("| 6. Delete Note                         |");
    puts("| 7. Exit                                |");
    puts("+========================================+");
    printf("> ");
}

int main(void)
{
	int choice = 0;

    setvbuf(stdin, 0, _IONBF, 0); 
    setvbuf(stdout, 0, _IONBF, 0);

	while (1)
	{
		menu();
		scanf("%d", &choice);
		switch (choice)
		{
		case 1:
			read_note();
			break;
		case 2:
			write_rdonly_note();
			break;
		case 3:
			write_rdwr_note();
			break;
		case 4:
			rewrite_rdwr_note();
			break;
		case 5:
			merge_rdonly_note();
			break;
		case 6:
			delete_note();
			break;
		case 7:
			exit(0);
			break;
		default:
			printf("Invalid choice OwO\n");
			break;
		}
	}

	return 0;
}
