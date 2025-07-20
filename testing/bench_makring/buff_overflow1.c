#include <stdio.h>
#include <string.h>

void process_input(char *input) {
    char buffer[10];
    strcpy(buffer, input); 
    printf("Processed input: %s\n", buffer);
}

void display_message(char *message) {
    char buffer[50];
    strncpy(buffer, message, sizeof(buffer) - 1); 
    buffer[sizeof(buffer) - 1] = '\0'; 
    printf("Displayed message: %s\n", buffer);
}

int main() {
    char user_input[100];

    printf("Enter a short message (safe function): ");
    fgets(user_input, sizeof(user_input), stdin);
    user_input[strcspn(user_input, "\n")] = '\0'; 
    display_message(user_input); 

    printf("Enter another message (vulnerable function): ");
    fgets(user_input, sizeof(user_input), stdin);
    user_input[strcspn(user_input, "\n")] = '\0'; 
    process_input(user_input); 

    return 0;
}