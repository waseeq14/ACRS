#include <stdio.h>
#include <string.h>

#define MAX_INPUT 100
#define MAX_USERNAME 50
#define MAX_DESC 10

typedef struct {
    char username[MAX_USERNAME];
    char description[MAX_DESC];
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
    strncpy(user->username, input, MAX_USERNAME - 1);
    user->username[MAX_USERNAME - 1] = '\0';
    
    printf("Enter description: ");
    fgets(input, MAX_INPUT, stdin);
    input[strcspn(input, "\n")] = '\0';
    strncpy(user->description, input, MAX_DESC - 1);
    user->description[MAX_DESC - 1] = '\0';
    
    write_to_file(user);
}

void edit_description(User *user) {
    char input[MAX_INPUT];
    int index;
    
    printf("Enter index to read description character (0-99): ");
    fgets(input, MAX_INPUT, stdin);
    sscanf(input, "%d", &index);
    printf("Character at index %d: %c\n", index, user->description[index]); // Out-of-bounds read: index may exceed MAX_DESC
}

void display_user(User *user) {
    printf("Username: %s, Description: %s\n", user->username, user->description);
}

int main() {
    User user = {{0}, {0}};
    int choice;
    char buffer[MAX_INPUT];

    while (1) {
        printf("\nMenu:\n1. Create User\n2. Edit Description\n3. Display User\n4. Exit\n");
        printf("Enter choice: ");
        fgets(buffer, MAX_INPUT, stdin);
        sscanf(buffer, "%d", &choice);

        switch (choice) {
            case 1:
                create_user(&user);
                break;
            case 2:
                if (user.username[0] != '\0') {
                    edit_description(&user);
                } else {
                    printf("No user created yet.\n");
                }
                break;
            case 3:
                if (user.username[0] != '\0') {
                    display_user(&user);
                } else {
                    printf("No user created yet.\n");
                }
                break;
            case 4:
                printf("Exiting.\n");
                return 0;
            default:
                printf("Invalid choice.\n");
        }
    }
}