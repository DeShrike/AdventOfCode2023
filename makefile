CC=gcc
AR=ar

all: startday-c

rmbin:
	startday-c

#########################################

startday-c: startday-c.o
	$(CC) -o startday-c startday-c.o

startday-c.o: startday-c.c
	$(CC) -c -O3 startday-c.c

#############################################

clean:
	rm *.o
