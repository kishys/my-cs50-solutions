// Cash Less

#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>
#include <string.h>

int main(void)
{
    int counter = 0;

    int ans = -1;
    while (ans < 0)
    {
        ans = get_int("Change Owed ");
    }

    while (ans >= 25)
    {
        ans -= 25;
        counter++;
    }

    while (ans >= 10)
    {
        ans -= 10;
        counter++;
    }

    while (ans >= 5)
    {
        ans -= 5;
        counter++;
    }

    while (ans > 0)
    {
        ans -= 1;
        counter++;
    }

    printf("%d\n", counter);

    return 0;
}
