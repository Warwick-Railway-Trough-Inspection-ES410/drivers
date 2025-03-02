#include <stdlib.h>
#include <stdio.h>
#include <dma_pwm.h>

int main(int argc, char *argv[])
{
    if (argc != 4)
    {
        return -1;
    }
    int channel_id = atoi(argv[0]);
    int gpio_val = atoi(argv[1]);
    int gpio[1] = {gpio_val};
    float freq = atof(argv[2]);
    float duty = atof(argv[3]);

    int result = set_pwm(channel_id, gpio, sizeof(gpio) / sizeof(int), freq, duty);
    return result;
}