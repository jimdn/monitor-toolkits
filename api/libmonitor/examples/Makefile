BINARY=monitor_example
SOURCE=$(wildcard *.c)
OBJ=$(patsubst %.c, %.o, $(SOURCE))

INC=-I ../src
LIB=../src/libmonitor.a

CFLAGS=-g -Wall -fPIC
CC=gcc

all:$(BINARY) 

%.o:%.c
	$(CC) $(CFLAGS) $(INC) -o $@ -c $<

$(BINARY):$(OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)

clean:
	rm -rf $(BINARY) *.o

.PHONY: all clean
