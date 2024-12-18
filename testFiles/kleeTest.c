#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to reverse a string
void reverse_string(char *str) {
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++) {
        char temp = str[i];
        str[i] = str[len - i - 1];
        str[len - i - 1] = temp;
    }
}

// Function to calculate the sum of an array
int sum_array(int *arr, int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}

// Function with a potential out-of-bounds read vulnerability
void read_array(int *arr, int size, int index) {
    printf("Reading from array at index %d...\n", index);
    // Vulnerability: No boundary check for 'index'
    printf("Value: %d\n", arr[index]);
     
}

// Function to copy a string safely
void copy_string(char *dest, const char *src, size_t max_len) {
    strncpy(dest, src, max_len - 1);
    dest[max_len - 1] = '\0';
}

// Main function
int main() {
    // Demonstrating string manipulation
    char str[50] = "Hello, World!";
    printf("Original string: %s\n", str);
    reverse_string(str);
    printf("Reversed string: %s\n", str);

    // Demonstrating array summation
    int numbers[] = {1, 2, 3, 4, 5};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    printf("Sum of array: %d\n", sum_array(numbers, size));

    // Out-of-bounds read demonstration
    int index;
    printf("Enter an index to read from the array (0 to %d): ", size - 1);
    scanf("%d", &index);
    read_array(numbers, size, index);

    // Demonstrating safe string copy
    char dest[50];
    copy_string(dest, str, sizeof(dest));
    printf("Copied string: %s\n", dest);

    return 0;
}
