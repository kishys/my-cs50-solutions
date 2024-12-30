#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(void)
{

    char letters[26] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};
    int values[26] = {1, 3, 3, 2,  1, 4, 2, 4, 1, 8, 5, 1, 3,
                      1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

    string playerone = get_string("Player 1: ");
    int counterone = 0;
    string playertwo = get_string("Player 2: ");
    int countertwo = 0;

    for (int i = 0; playerone[i] != '\0'; i++)
    {

        char c = tolower(playerone[i]);

        for (int j = 0; j < 26; j++)
        {
            if (c == letters[j])
            {
                counterone += values[j];
                break;
            }
        }
    }

    for (int i = 0; playertwo[i] != '\0'; i++)
    {

        char c = tolower(playertwo[i]);

        for (int j = 0; j < 26; j++)
        {
            if (c == letters[j])
            {
                countertwo += values[j];
                break;
            }
        }
    }

    if (counterone > countertwo)
    {
        printf("Player 1 wins!");
    }

    if (counterone < countertwo)
    {
        printf("Player 2 wins!");
    }
    if (counterone == countertwo)
    {
        printf("Tie!");
    }
}
