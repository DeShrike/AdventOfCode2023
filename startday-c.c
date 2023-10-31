#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#define MAX_LINE_LENGTH 256
#define C_TEMPLATE   "./template.c.txt"
#define MAKEFILE     "./c/makefile"
#define MAKEFILE_TEMP     "./makefile.tmp"
#define MAX_TEMPLATE_LINES 100

#define C_FILE       "./c/day%d.c"

#define MARKER_ALL		"# ALL"
#define MARKER_RMBIN	"# RMBIN"
#define MARKER_START	"# START"
#define MARKER_END		"# END"

char *template_line[MAX_TEMPLATE_LINES] = { NULL };

int file_exists(const char *filename)
{
	if (!access(filename, F_OK))
	{
		return 1;
	}

	return 0;
}

void replace1(char *string, char *search, char *replaceby)
{
	char temp[MAX_LINE_LENGTH];
	char *rest;
	char *found = strstr(string, search);
	if (found == NULL)
	{
		return;
	}

	rest = found + strlen(search);
	strcpy(temp, rest);
	strcpy(found, replaceby);
	rest = found + strlen(replaceby);
	strcpy(rest, temp);
}

void replace(char *string, char *search, char *replaceby)
{
	while (strstr(string, search) != NULL)
	{
		replace1(string, search, replaceby);
	}
}

void write_template(int day)
{
	char day_string[10];
	sprintf(day_string, "%d", day);

	char c_filename[100];
	sprintf(c_filename, C_FILE, day);

	printf("Writing %s\n", c_filename);

	FILE *fp, *fo;
	fp = fopen(C_TEMPLATE, "r");
	fo = fopen(c_filename, "w");

	char buffer[MAX_LINE_LENGTH];
	while (fgets(buffer, MAX_LINE_LENGTH, fp))
	{
		buffer[strcspn(buffer, "\n")] = 0;
		buffer[strcspn(buffer, "\r")] = 0;
		replace(buffer, "%DAY%", day_string);
		fprintf(fo, "%s\n", buffer);
	}

	fclose(fo);
	fclose(fp);
}

enum { NORMAL, NEXT_ALL, NEXT_ALL2, NEXT_RMBIN, NEXT_RMBIN2, IN_TEMPLATE, AFTER_TEMPLATE };

void rewrite_makefile(int day)
{
	int template_size = 0;
	char all_string[100];
	char day_string[100];
	char rmbin_string[100];

	sprintf(all_string, " day%d", day);
	sprintf(day_string, "%d", day);
	sprintf(rmbin_string, "\trm day%d", day);

	FILE *fp, *fo;
	fp = fopen(MAKEFILE, "r");
	fo = fopen(MAKEFILE_TEMP, "w");

	int mode = NORMAL;
	char buffer[MAX_LINE_LENGTH];
	while (fgets(buffer, MAX_LINE_LENGTH, fp))
	{
		buffer[strcspn(buffer, "\n")] = 0;
		buffer[strcspn(buffer, "\r")] = 0;

		if (strstr(buffer, MARKER_ALL) != NULL)
		{
			mode = NEXT_ALL;
		}
		else if (strstr(buffer, MARKER_RMBIN) != NULL)
		{
			mode = NEXT_RMBIN;
		}
		else if (strstr(buffer, MARKER_START) != NULL)
		{
			mode = IN_TEMPLATE;
		}

		if (mode != IN_TEMPLATE)
		{
			replace(buffer, "%DAY%", day_string);
		}

		if (mode == NEXT_ALL)
		{
			fprintf(fo, "%s\n", buffer);

			mode = NEXT_ALL2;
		}
		else if (mode == NEXT_ALL2)
		{
			strcat(buffer, all_string);
			fprintf(fo, "%s\n", buffer);

			mode = NORMAL;
		}
		else if (mode == NEXT_RMBIN)
		{
			fprintf(fo, "%s\n", buffer);
			mode = NEXT_RMBIN2;
		}
		else if (mode == NEXT_RMBIN2)
		{
			fprintf(fo, "%s\n", buffer);
			fprintf(fo, "%s\n", rmbin_string);
			mode = NORMAL;
		}
		else if (mode == IN_TEMPLATE)
		{
			fprintf(fo, "%s\n", buffer);
			if (strstr(buffer, MARKER_START) == NULL && strstr(buffer, MARKER_END) == NULL)
			{
				template_line[template_size] = malloc(strlen(buffer) * 2);
				strcpy(template_line[template_size], buffer);
				template_size++;
			}
		}
		else if (mode == NORMAL)
		{
			fprintf(fo, "%s\n", buffer);
		}

		if (strstr(buffer, MARKER_END) != NULL)
		{
			mode = NORMAL;
		}
	}

	fprintf(fo, "\n");
	int i = 0;
	while (template_line[i] != NULL)
	{
		replace(template_line[i], "%DAY%", day_string);
		fprintf(fo, "%s\n", template_line[i]);
		i++;
	}

	fclose(fo);
	fclose(fp);

	if (remove(MAKEFILE) != 0)
	{
		fprintf(stderr, "ERROR: Could not delete file %s. %s\n", MAKEFILE, strerror(errno));
		exit(6);
	}

	if (rename(MAKEFILE_TEMP, MAKEFILE) != 0)
	{
		fprintf(stderr, "ERROR: Rename %s to %s failed. %s\n", MAKEFILE_TEMP, MAKEFILE, strerror(errno));
		exit(7);
	}

	for (int i = 0; i < MAX_TEMPLATE_LINES; ++i)
	{
		if (template_line[i] != NULL)
		{
			free(template_line[i]);
		}
	}
}

void show_usage(const char* program)
{
	printf("Usage: %s <day>\n", program);
}

int main(int argc, char **argv)
{
	if (argc != 2)
	{
		show_usage(argv[0]);
		exit(1);
	}

	int day = atoi(argv[1]);
	if (day < 1 || day > 25)
	{
		fprintf(stderr, "ERROR: <day> must be a number from 1 to 25\n");
		show_usage(argv[0]);
		exit(2);
	}

	if (file_exists(MAKEFILE) == 0)
	{
		fprintf(stderr, "ERROR: File %s not found !\n", MAKEFILE);
		exit(4);
	}

	if (file_exists(C_TEMPLATE) == 0)
	{
		fprintf(stderr, "ERROR: File %s not found !\n", C_TEMPLATE);
		exit(5);
	}

	char c_file[200];
	sprintf(c_file, C_FILE, day);
	if (file_exists(c_file) == 1)
	{
		fprintf(stderr, "ERROR: File %s already exists !\n", c_file);
		exit(3);
	}

	write_template(day);
	rewrite_makefile(day);

	return 0;
}

