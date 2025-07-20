//Case2:
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_INPUT 100

typedef struct {
    char *username;
    char *description;
} User;

void write_to_file(User *user) {
    FILE *file = fopen("user_data.txt", "a");
    if (file == NULL) {
        printf("Error opening file!\n");
        return;
    }
    fprintf(file, "Username: %s, Description: %s\n", user->username, user->description);
    fclose(file);
    printf("Data written to file.\n");
}

void create_user(User *user) {
    char input[MAX_INPUT];
    
    printf("Enter username: ");
    fgets(input, MAX_INPUT, stdin);
    input[strcspn(input, "\n")] = '\0';
    user->username = malloc(strlen(input) + 1);
    strcpy(user->username, input);
    
    printf("Enter description: ");
    fgets(input, MAX_INPUT, stdin);
    input[strcspn(input, "\n")] = '\0';
    user->description = malloc(strlen(input) + 1);
    strcpy(user->description, input);
    
    write_to_file(user);
}

void edit_description(User *user) {
    char input[MAX_INPUT];
    char *new_buffer = malloc(10);
    
    printf("Enter new description: ");
    fgets(input, MAX_INPUT, stdin);
    input[strcspn(input, "\n")] = '\0';
    strcpy(new_buffer, input); //Safe Code, ALL good here
    free(user->description);
    user->description = new_buffer;
    user->description = NULL; 
    printf("Description updated.\n");
}

void display_user(User *user) {
    printf("Username: %s, Description: %s\n", user->username, user->description);
}

void free_user(User *user) {
    free(user->username);
    free(user->description);
    user->username = NULL;
    user->description = NULL;
}

int main() {
    User user = {NULL, NULL};
    int choice;
    char buffer[MAX_INPUT];

    while (1) {
        printf("\nMenu:\n1. Create User\n2. Edit Description\n3. Display User\n4. Exit\n");
        printf("Enter choice: ");
        fgets(buffer, MAX_INPUT, stdin);
        sscanf(buffer, "%d", &choice);

        switch (choice) {
            case 1:
                if (user.username != NULL || user.description != NULL) {
                    free_user(&user);
                }
                create_user(&user);
                break;
            case 2:
                if (user.description != NULL) {
                    edit_description(&user);
                } else {
                    printf("No user created yet.\n");
                }
                break;
            case 3:
                if (user.username != NULL && user.description != NULL) {
                    display_user(&user);
                } else {
                    printf("No user created yet.\n");
                }
                break;
            case 4:
                free_user(&user);
                printf("Exiting.\n");
                return 0;
            default:
                printf("Invalid choice.\n");
        }
    }
}