#include <stdio.h>
#include <stdlib.h>

int findLargest(int a, int b) {
    return (a > b) ? a : b;
}

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    int x = 25;
    int y = 73;
    int largest;

    largest = findLargest(x, y);

    swap(&x, &y);

    FILE *file = fopen("output.txt", "w");
    if (file == NULL) {
        return 1;
    }

    char buffer[1024];
    setvbuf(file, buffer, _IOFBF, sizeof(buffer));

    int *numbers = (int *)malloc(5 * sizeof(int));
    if (numbers == NULL) {
        fclose(file);
        return 1;
    }

    for (int i = 0; i < 5; i++) {
        *(numbers + i) = (i + 1) * 15;
    }

    int j = 0;
    while (j < 5) {
        fprintf(file, "Array index %d: %d\n", j, *(numbers + j));
        j++;
    }

    fprintf(file, "Largest of original values: %d\n", largest);
    fprintf(file, "Swapped values: x = %d, y = %d\n", x, y);

    fflush(file);
    fclose(file);
    free(numbers);

    return 0;
}