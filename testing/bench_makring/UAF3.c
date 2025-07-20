#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MIN_VALUE 100

void display(int* ptr) {
    printf("You entered: %d\n", *ptr);  // UAF here if ptr is freed
}

int main() {
    int* value = malloc(sizeof(int));
    if (!value) {
        perror("malloc failed");
        return 1;
    }

    printf("Enter a value >= %d:\n> ", MIN_VALUE);
    scanf("%d", value);

    if (*value < MIN_VALUE) {
        printf("Value too small! Try again:\n> ");
        free(value);  // Frees memory
        scanf("%d", value); 
    }
    display(value);

    free(value); 

    return 0;
}