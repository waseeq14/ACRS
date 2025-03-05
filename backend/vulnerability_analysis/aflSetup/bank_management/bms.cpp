#include <iostream>
#include <fstream>
#include <cstring>
#include <cstdlib>

class BankAccount {
public:
    char accountHolder[16]; // Fixed-size buffer (Potential overflow)
    int balance;

    BankAccount(const char* name, int initialBalance) {
        strncpy(accountHolder, name, sizeof(accountHolder) - 1);
        accountHolder[sizeof(accountHolder) - 1] = '\0';
        balance = initialBalance;
    }

    void deposit(int amount) {
        if (amount > 0) {
            balance += amount;
            std::cout << "Deposited $" << amount << ". New Balance: $" << balance << "\n";
        }
    }

    void withdraw(int amount) {
        if (amount > balance) {
            std::cout << "Insufficient funds!\n";
        } else {
            balance -= amount;
            std::cout << "Withdrawn $" << amount << ". New Balance: $" << balance << "\n";
        }
    }
};

// Global pointer for Use-After-Free vulnerability
BankAccount* account = nullptr;

void processTransaction(const char* input) {
    char buffer[32];  // Vulnerable buffer
    strcpy(buffer, input); // 💥 Potential Buffer Overflow 💥

    if (strncmp(buffer, "CREATE ", 7) == 0) {
        if (account) delete account; // Clean up existing account
        account = new BankAccount(buffer + 7, 100); // Default $100
        std::cout << "Account created for: " << account->accountHolder << "\n";
    } else if (strncmp(buffer, "DEPOSIT ", 8) == 0) {
        int amount = atoi(buffer + 8);
        account->deposit(amount);
    } else if (strncmp(buffer, "WITHDRAW ", 9) == 0) {
        int amount = atoi(buffer + 9);
        account->withdraw(amount);
    } else if (strncmp(buffer, "DELETE", 6) == 0) {
        delete account;
        std::cout << "Account deleted.\n";
    } else {
        std::cout << "Invalid command!\n";
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <input_file>\n";
        return 1;
    }

    std::ifstream file(argv[1], std::ios::binary);
    if (!file) {
        std::cerr << "Error opening file!\n";
        return 1;
    }

    std::string input((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    processTransaction(input.c_str());

    return 0;
}
