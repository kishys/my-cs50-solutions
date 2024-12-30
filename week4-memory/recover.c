/*
https://cs50.harvard.edu/x/2023/psets/4/recover/
*/

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover filename.raw\n");
        return 1;
    }
    FILE *file = fopen(argv[1], "r");

    if (file == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    typedef uint8_t BYTE;
    BYTE buffer[BLOCK_SIZE];

    int counter = 0;

    char *filename = malloc(8 * sizeof(char));

    FILE *output = NULL;

    while (fread(buffer, 1, BLOCK_SIZE, file) == BLOCK_SIZE)
    {

        if (buffer[0] == 0xFF && buffer[1] == 0xD8 && buffer[2] == 0xFF &&
            (buffer[3] & 0xF0) == 0xE0)
        {

            if (counter == 0)
            {

                sprintf(filename, "%03i.jpg", counter);
                output = fopen(filename, "w");
                fwrite(buffer, 1, BLOCK_SIZE, output);

                counter++;
            }

            else if (counter > 0)
            {
                fclose(output);
                sprintf(filename, "%03i.jpg", counter);
                output = fopen(filename, "w");
                fwrite(buffer, 1, BLOCK_SIZE, output);
                counter++;
            }
        }

        else if (counter > 0)
        {

            fwrite(buffer, 1, BLOCK_SIZE, output);
        }
    }

    free(filename);
    fclose(file);
    fclose(output);
}
