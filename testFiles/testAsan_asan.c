#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void processData(char *buffer) {
    // Simulate some processing
    printf("Processing data: %s\n", buffer);
}

void freeData(char *buffer) {
    free(buffer);
    printf("Memory has been freed.\n");
}

int main() {
    char *data;

    // Step 1: Allocate memory
    data = (char *)malloc(100 * sizeof(char));
    if (data == NULL) {
        perror("malloc");
        return 1;
    }

    // Step 2: Use the allocated memory
    strcpy(data, "Hidden Use After Free vulnerability.");
    printf("Data before free: %s\n", data);

    // Step 3: Process data and free memory
    processData(data);
    freeData(data);

    // Step 4: Indirect access to freed memory (Use After Free)
    processData(data); // Hidden UAF via function call

    return 0;
}