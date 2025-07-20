#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <klee/klee.h>

unsigned int getRand()
{
	unsigned int r;
	klee_make_symbolic(&r, sizeof(r), "r");
	return r;
}

unsigned plop() {
	return getRand() % 256 + 127;
}

int main()
{
	char buffer[256];
	memset(buffer, 0, sizeof(buffer));
	buffer[plop()] = '!';
	klee_print_expr("Buffer content:", buffer[0]);
	return 0;
}