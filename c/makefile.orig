CC=gcc
AR=ar

# ALL
all: 

# RMBIN
rmbin:

#########################################

aoc.o: aoc.c aoc.h
	$(CC) -c -O3 aoc.c

#############################################

clean:
	rm *.o

# START
#############################################

day%DAY%: day%DAY%.o aoc.o
	$(CC) -o day%DAY% day%DAY%.o aoc.o

day%DAY%.o: day%DAY%.c aoc.h
	$(CC) -c -O3 day%DAY%.c

#############################################
# END
