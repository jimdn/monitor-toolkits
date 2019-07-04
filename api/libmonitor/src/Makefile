LIBOUT=libmonitor.a
SOURCE=$(wildcard *.c)
OBJ=$(patsubst %.c, %.o, $(SOURCE))

CFLAGS=-g -Wall -fPIC
CC=gcc

all:$(LIBOUT) 

$(LIBOUT):$(OBJ)
	ar -rs $(LIBOUT) $(OBJ)

%.o:%.c
	$(CC) $(CFLAGS) -o $@ -c $<

clean:
	rm -rf $(LIBOUT) *.o

.PHONY: all clean
