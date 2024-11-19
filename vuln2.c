#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int id;
    char name[50];
} Person;

void free_memory(Person **p) {
    if (*p != NULL) {
        printf("Freeing memory for %s\n", (*p)->name);
        free(*p);
        *p = NULL;  // Nullify the pointer after freeing
    }
}

void use_after_free(Person *p) {
    printf("Using freed memory: %s\n", p->name);  // UAF occurs here
}

void double_free(Person *p) {
    printf("Freeing memory again: %s\n", p->name);
    free(p);  // Double-free occurs here
}

int main() {
    // Allocate memory for two Person structures
    Person *person1 = (Person *)malloc(sizeof(Person));
    Person *person2 = (Person *)malloc(sizeof(Person));

    if (person1 == NULL || person2 == NULL) {
        printf("Memory allocation failed\n");
        return 1;
    }

    // Initialize the person structs
    person1->id = 1;
    strcpy(person1->name, "Alice");

    person2->id = 2;
    strcpy(person2->name, "Bob");

    // Free memory for person1 (First Free)
    free_memory(&person1);

    // The following line introduces a Use-After-Free (UAF) vulnerability
    use_after_free(person1);  // person1 is already freed

    // After the first free, person2 is still valid
    printf("Person 2: %s\n", person2->name);

    // Now let's introduce Double-Free vulnerability:
    // Free memory for person2 (First Free)
    free_memory(&person2);

    // Double free of person2 (Second Free)
    double_free(person2);  // This is the Double-Free

    return 0;
}
    