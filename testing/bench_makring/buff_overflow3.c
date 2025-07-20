//Case3:
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
    char user_input1[100];
    char user_input2[100];

    printf("Enter a short message (safe function): ");
    fgets(user_input1, sizeof(user_input1), stdin);
    user_input1[strcspn(user_input1, "\n")] = '\0'; 
    display_message(user_input1);

    printf("Enter another message (vulnerable function): ");
    fgets(user_input2, sizeof(user_input2), stdin);
    user_input2[strcspn(user_input2, "\n")] = '\0'; 
    process_input(user_input2);

    printf("First input was: %s\n", user_input1);

    return 0;
}