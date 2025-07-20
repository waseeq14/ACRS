#include <stdio.h>
#include <string.h>

#define MAX_INPUT 100

void encrypt_inputs(char *key, char *secret, char *result) {
    int i;
    for (i = 0; key[i] != '\0' && secret[i] != '\0' && i < MAX_INPUT - 1; i++) {
        result[i] = key[i] ^ secret[i];
    }
    result[i] = '\0';
    printf("Encrypted result (inputs): %s\n", result);
}

void encrypt_with_secret(char *key, char *result) {
    char *secret = NULL;
    int i;
    for (i = 0; key[i] != '\0' && i < MAX_INPUT - 1; i++) {
        result[i] = key[i] ^ secret[i]; // NULL pointer dereference: secret is NULL
    }
    result[i] = '\0';
    printf("Encrypted result (secret): %s\n", result);
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