#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_INPUT 100

void verify_entry(char *input) {
    char *buffer = malloc(50);
    strncpy(buffer, input, 49);
    buffer[49] = '\0';
    printf("Verified entry: %s\n", buffer);
    free(buffer);
}

Case4:
void process_record(char *input) {
    char *record = malloc(10);
    strncpy(record, input, 9);
    record[9] = '\0';
    free(record);
    printf("Processed record: %s\n", record); // Use-After-Free: accessing record after free
}

int main() {
    char input[MAX_INPUT];
    
    printf("Enter input for entry verification: ");
    fgets(input, MAX_INPUT, stdin);
    input[strcspn(input, "\n")] = '\0';
    verify_entry(input);
    
    printf("Enter input for record processing: ");
    fgets(input, MAX_INPUT, stdin);
    input[strcspn(input, "\n")] = '\0';
    process_record(input);
    
    return 0;
}
