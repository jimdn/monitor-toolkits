all: lib example

lib:
	@echo "Compiling $@"
	make -C src

example:
	@echo "Compiling $@"
	make -C example

clean:
	make -C src clean
	make -C example clean

.PHONY: all lib example clean
