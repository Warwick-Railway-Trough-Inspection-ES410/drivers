#include <stdlib.h>
#include <stdio.h>
#include <dma_pwm.h>

int main(int argc, char *argv[])
{
    if (argc != 1)
    {
        return -1;
    }

    int channel_id = atoi(argv[0]);

    int result = free_pwm(channel_id);
    return result;
}