#include <dma_pwm.h>

int main()
{
    int result = config_pwm(DEFAULT_PAGES, DEFAULT_PULSE_WIDTH);
    return result;
}