#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <gnu/libc-version.h>
#include <assert.h>

int main()
{
    char *p = malloc(0x100);
    free(p);
    free(p);
    malloc(0x100);
    malloc(0x100);
    malloc(0x100);

    getchar();
    
    return 0;
}