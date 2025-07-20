#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_INPUT 100

void display_credentials(char *username, char *password) {
    char *temp = malloc(50);
    strncpy(temp, username, 49);
    temp[49] = '\0';
    printf("Credentials - Username: %s, Password: %s\n", temp, password);
    free(temp);
}

void verify_credentials(char *username, char *password) {
    char *user_buffer = malloc(10); // Small heap buffer for username
    char *pass_buffer = malloc(50); // Adjacent heap buffer for password
    strcpy(user_buffer, username); // Heap-based buffer overflow: username can overwrite pass_buffer
    strncpy(pass_buffer, password, 49);
    pass_buffer[49] = '\0';
    printf("Verification - Username: %s, Password: %s\n", user_buffer, pass_buffer);
    free(user_buffer);
    free(pass_buffer);
}

int main() {
    char username[MAX_INPUT];
    char password[MAX_INPUT];
    
    printf("Enter username: ");
    fgets(username, MAX_INPUT, stdin);
    username[strcspn(username, "\n")] = '\0';
    
    printf("Enter password: ");
    fgets(password, MAX_INPUT, stdin);
    password[strcspn(password, "\n")] = '\0';
    
    display_credentials(username, password);
    verify_credentials(username, password);
    
    return 0;
}