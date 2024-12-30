#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    int letters = 0;
    int words = 1;
    int sentences = 0;

    char punctuation[3] = {'.', '!', '?'};

    string checker = get_string("Text: ");
    int length = strlen(checker);

    for (int i = 0; i < length; i++)
    {
        if (isalpha(checker[i]))
        {
            letters++;
        }

        for (int k = 0; k < 3; k++)
        {
            if (checker[i] == punctuation[k])
            {
                sentences++;
            }
        }

        if (checker[i] == ' ')
        {
            words++;
        }
    }

    double L = (letters / (double) words) * 100;
    double S = (sentences / (double) words) * 100;
    double index = 0.0588 * L - 0.296 * S - 15.8;

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        int findex = round(index);
        printf("Grade %d\n", findex);
    }
}
