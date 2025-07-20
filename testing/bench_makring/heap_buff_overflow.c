#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_INPUT 100

void encrypt_inputs(char *key, char *secret, char *result) {
    char *buffer = malloc(MAX_INPUT);
    int i;
    for (i = 0; key[i] != '\0' && secret[i] != '\0' && i < MAX_INPUT - 1; i++) {
        buffer[i] = key[i] ^ secret[i];
    }
    buffer[i] = '\0';
    strncpy(result, buffer, MAX_INPUT - 1);
    result[MAX_INPUT - 1] = '\0';
    printf("Encrypted result (inputs): %s\n", result);
    free(buffer);
}

void encrypt_with_secret(char *key, char *result) {
    char *buffer = malloc(10);
    strcpy(buffer, key); // Heap-based buffer overflow: No bounds checking, can write beyond 10 bytes
    int i;
    for (i = 0; buffer[i] != '\0' && i < MAX_INPUT - 1; i++) {
        result[i] = buffer[i] ^ 'S';
    }
    result[i] = '\0';
    printf("Encrypted result (secret): %s\n", result);
    free(buffer);
}

int main() {
    char key[MAX_INPUT];
    char secret[MAX_INPUT];
    char result[MAX_INPUT];
    
    printf("Enter key: ");
    fgets(key, MAX_INPUT, stdin);
    key[strcspn(key, "\n")] = '\0';
    
    printf("Enter secret: ");
    fgets(secret, MAX_INPUT, stdin);
    secret[strcspn(secret, "\n")] = '\0';
    
    encrypt_inputs(key, secret, result);
    encrypt_with_secret(key, result);
    
    return 0;
}