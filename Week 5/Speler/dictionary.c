/*
https://cs50.harvard.edu/x/2023/psets/5/speller/
*/

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

const unsigned int N = 1000;

int counter = 0;

node *table[N];

bool check(const char *word)
{
    int index = hash(word);
    node *cursor = table[index];

    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) != 0)
        {
            cursor = cursor->next;
        }
        else
        {
            return true;
        }
    }

    return false;
}

unsigned int hash(const char *word)
{
    int points = 0;

    for (int i = 0, len = strlen(word); i < len; i++)
    {
        points += toupper(word[i]) - 'A';
    }

    return points % N;
}

bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");

    if (file == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];

    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            return false;
        }

        strcpy(n->word, word);
        n->next = NULL;

        int index = hash(word);

        n->next = table[index];
        table[index] = n;
        counter++;
    }

    fclose(file);

    return true;
}

unsigned int size(void)
{
    return counter;
}

bool unload(void)
{
    node *cursor = NULL;

    for (int i = 0; i < N; i++)
    {
        cursor = table[i];

        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;

            free(temp);
        }
    }

    return true;
}
