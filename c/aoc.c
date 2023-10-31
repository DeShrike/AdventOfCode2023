#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>
#include "aoc.h"

clock_t start, end;
double cpu_time_used;

int part = 0;
long long answer_a = 0;
long long answer_b = 0;

char Reversed[] =      "\033[7m";
char DimBackground[] = "\033[5m";
char Reset[] =         "\033[0m";

char ClearScreen[] =   "\033[2J";
char ClearLine[] =     "\033[2K";

char HideCursor[] =    "\033[?25l";
char ShowCursor[] =    "\033[?25h";

char BrightBlack[] =   "\033[30;1m";
char BrightRed[] =     "\033[31;1m";
char BrightGreen[] =   "\033[32;1m";
char BrightYellow[] =  "\033[33;1m";
char BrightBlue[] =    "\033[34;1m";
char BrightMagenta[] = "\033[35;1m";
char BrightCyan[] =    "\033[36;1m";
char BrightWhite[] =   "\033[37;1m";

void start_day(int day)
{
	printf("%s %sDay %s%d %s\n\n", DimBackground, BrightWhite, BrightYellow, day, Reset);
}

void start_part_a()
{
	printf("%sPart %sA%s\n", BrightWhite, BrightCyan, Reset);
	part = 1;
    start = clock();
}

void start_part_b()
{
	printf("%sPart %sB%s\n", BrightWhite, BrightCyan, Reset);
	part = 2;
    start = clock();
}

long long get_answer_a()
{
	return answer_a;
}

long long get_answer_b()
{
	return answer_b;
}

void show_answer(long long answer)
{
    end = clock();

	if (part == 1)
	{
		answer_a = answer;
		printf("Answer: %s%lld%s", BrightGreen, answer_a, Reset);
	}
	else if (part == 2)
	{
		answer_b = answer;
		printf("Answer: %s%lld%s", BrightGreen, answer_b, Reset);
	}

    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
	printf(" | Took %s%f%s seconds\n\n", BrightMagenta, cpu_time_used, Reset);
}

void free_input(char** lines, int line_count)
{
	for (int i = 0; i < line_count; i++)
	{
		if (lines[i] != NULL)
		{
			free(lines[i]);
		}
	}

	free(lines);
}

char** read_input(int day, char* path, int max_lines, int max_line_length, int* line_count)
{
	char filename[100];
	sprintf(filename, "%sinput-day%d.txt", path, day);
	FILE *file = fopen(filename, "r");
	if (file == NULL)
	{
		fprintf(stderr, "Could not open file %s\n", filename);
		perror("fopen()");
		return NULL;
	}

	char** lines = (char**)malloc(max_lines * sizeof(char*));
	for (int i = 0; i < max_lines; i++)
	{
		lines[i] = NULL;
	}

	size_t len = max_line_length;
	char* line = (char* )malloc(len);
	ssize_t nread;
	while ((nread = getline(&line, &len, file)) != -1)
	{
		// printf("Retrieved line of length %zu:\n", nread);
		// fwrite(line, nread, 1, stdout);
		char* thisline = (char*)malloc(nread * sizeof(char));
		lines[(*line_count)] = thisline;
		strcpy(thisline, line);
		(*line_count)++;
	}

	free(line);
	fclose(file);
	return lines;
}

int* convert_input_to_numbers(char **lines, int line_count)
{
	int* numbers = (int*)malloc(line_count * sizeof(int));
	for (int ix = 0; ix < line_count; ix++)
	{
		numbers[ix] = atoi(lines[ix]);
	}

	return numbers;
}

char *ltrim(char *s)
{
    while (isspace(*s)) s++;
    return s;
}

char *rtrim(char *s)
{
    char* back = s + strlen(s);
    while (isspace(*--back));
    *(back+1) = '\0';
    return s;
}

char *trim(char *s)
{
    return rtrim(ltrim(s));
}
