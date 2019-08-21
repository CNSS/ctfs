#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>


int main()
{
    int fd = open("/sudrv.ko", O_RDONLY | O_WRONLY);
    if (fd < 0) return 0;


    return 0;
}