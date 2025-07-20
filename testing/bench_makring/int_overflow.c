#include <stdio.h>
#include <string.h>

#define MAX_INPUT 100
#define MAX_USERNAME 50

typedef struct {
    char username[MAX_USERNAME];
    unsigned int balance;
} Account;

void write_to_file(Account *account, char *transaction, unsigned int amount) {
    FILE *file = fopen("bank_transactions.txt", "a");
    if (file == NULL) {
        printf("Error opening file!\n");
        return;
    }
    fprintf(file, "Username: %s, Transaction: %s, Amount: %u, Balance: %u\n", 
            account->username, transaction, amount, account->balance);
    fclose(file);
    printf("Transaction recorded.\n");
}

void create_user(Account *account) {
    char input[MAX_INPUT];
    
    printf("Enter username: ");
    fgets(input, MAX_INPUT, stdin);
    input[strcspn(input, "\n")] = '\0';
    strncpy(account->username, input, MAX_USERNAME - 1);
    account->username[MAX_USERNAME - 1] = '\0';
    account->balance = 0;
    printf("User created.\n");
}

void deposit_money(Account *account) {
    char input[MAX_INPUT];
    unsigned int amount;
    
    printf("Enter amount to deposit: ");
    fgets(input, MAX_INPUT, stdin);
    sscanf(input, "%u", &amount);
    account->balance = account->balance + amount; // Integer overflow: No check for sum exceeding UINT_MAX
    printf("Deposited %u. New balance: %u\n", amount, account->balance);
    write_to_file(account, "Deposit", amount);
}

void withdraw_money(Account *account) {
    char input[MAX_INPUT];
    unsigned int amount;
    
    printf("Enter amount to withdraw: ");
    fgets(input, MAX_INPUT, stdin);
    sscanf(input, "%u", &amount);
    if (amount <= account->balance) {
        account->balance -= amount;
        printf("Withdrew %u. New balance: %u\n", amount, account->balance);
        write_to_file(account, "Withdraw", amount);
    } else {
        printf("Insufficient balance.\n");
    }
}

void display_balance(Account *account) {
    printf("Username: %s, Balance: %u\n", account->username, account->balance);
}

int main() {
    Account account = {{0}, 0};
    int choice;
    char buffer[MAX_INPUT];

    while (1) {
        printf("\nMenu:\n1. Create User\n2. Deposit Money\n3. Withdraw Money\n4. Display Balance\n5. Exit\n");
        printf("Enter choice: ");
        fgets(buffer, MAX_INPUT, stdin);
        sscanf(buffer, "%d", &choice);

        switch (choice) {
            case 1:
                create_user(&account);
                break;
            case 2:
                if (account.username[0] != '\0') {
                    deposit_money(&account);
                } else {
                    printf("No user created yet.\n");
                }
                break;
            case 3:
                if (account.username[0] != '\0') {
                    withdraw_money(&account);
                } else {
                    printf("No user created yet.\n");
                }
                break;
            case 4:
                if (account.username[0] != '\0') {
                    display_balance(&account);
                } else {
                    printf("No user created yet.\n");
                }
                break;
            case 5:
                printf("Exiting.\n");
                return 0;
            default:
                printf("Invalid choice.\n");
        }
    }
}