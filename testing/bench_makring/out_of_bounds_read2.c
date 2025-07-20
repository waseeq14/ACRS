//Case2:
#include <stdio.h>
#include <string.h>

#define MAX_INPUT 100
#define DATA_SIZE 10

void check_license(char *input) {
    char buffer[DATA_SIZE];
    strncpy(buffer, input, DATA_SIZE - 1);
    buffer[DATA_SIZE - 1] = '\0';
    printf("License check: %s\n", buffer);
}

void validate_data(char *input) {
    char data[DATA_SIZE] = "validate";
    int index;
    sscanf(input, "%d", &index);
    printf("Data at index %d: %c\n", index, data[index]); // Out-of-bounds read: index may exceed DATA_SIZE
}

int main() {
    char input[MAX_INPUT];
    
    printf("Enter input for license check: ");
    fgets(input, MAX_INPUT, stdin);
    input[strcspn(input, "\n")] = '\0';
    check_license(input);
    
    printf("Enter index for data validation: ");
    fgets(input, MAX_INPUT, stdin);
    validate_data(input);
    
    return 0;