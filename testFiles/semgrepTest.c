#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char name[50];
    int age;
    double salary;
    char department[30];
} Employee;

void display_employee_details(Employee *e) {
    printf("Name: %s\n", e->name);
    printf("Age: %d\n", e->age);
    printf("Salary: %.2f\n", e->salary);
    printf("Department: %s\n", e->department);
}

void modify_employee_details(Employee *e) {
    if (e == NULL) return;

    printf("Enter new name: ");
    fgets(e->name, sizeof(e->name), stdin);
    printf("name: ", e->name);

    printf("Enter new age: ");
    scanf("%d", &e->age);

    printf("Enter new salary: ");
    scanf("%lf", &e->salary);

    printf("Enter new department: ");
    fgets(e->department, sizeof(e->department), stdin);
}

void process_employee_data(char *name) {
    Employee *e = (Employee *)malloc(sizeof(Employee));
    if (e == NULL) {
        printf("Memory allocation failed!\n");
        return;
    }

    strncpy(e->name, name, sizeof(e->name) - 1);
    e->age = 25;
    e->salary = 55000.00;
    strncpy(e->department, "Engineering", sizeof(e->department) - 1);

    printf("Employee created. Initial details:\n");
    display_employee_details(e);

    modify_employee_details(e);

    free(e);

    printf("Attempting to access freed memory:\n");
    display_employee_details(e);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <employee_name>\n", argv[0]);
        return 1;
    }

    process_employee_data(argv[1]);

    return 0;
}
