#include <stdio.h>
#include <string.h>

#define	MAXSIZE		40
void
test(void)
{
	char buf[MAXSIZE];

	if(gets(buf))					
		printf("result: %s\n", buf);
}

int
main(int argc, char **argv)
{
	test();
	return 0;
}

