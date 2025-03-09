#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void buffer_overflow() {
    char buffer[10];
    gets(buffer); // Vulnerable function
    printf("Buffer: %s\n", buffer);
}

void integer_overflow() {
    int x = 2147483647; // Max int value
    int y = x + 1; // Integer overflow
    printf("Result: %d\n", y);
}

void use_after_free() {
    char *ptr = (char*)malloc(10);
    strcpy(ptr, "Hello");
    free(ptr);
    printf("After free: %s\n", ptr); // Use-after-free vulnerability
}

int main() {
    int choice;
    printf("Enter choice (1-3): ");
    scanf("%d", &choice);

    if (choice == 1)
        buffer_overflow();
    else if (choice == 2)
        integer_overflow();
    else if (choice == 3)
        use_after_free();
    
    return 0;
}
