// Mario Less

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int answer = 0;
    while (answer > 8 || answer < 1)
    {
        answer = get_int("Height? ");
    }

    int height = answer;

    for (int i = 1; i <= height; i++)
    {
        for (int j = height - i; j > 0; j--)
        {
            printf(" ");
        }

        for (int k = 0; k < i; k++)
        {
            printf("#");
        }
        printf("\n");
    }
    return 0;
}
