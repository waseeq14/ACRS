#include <klee/klee.h>
#include <string.h>

void reverse_string(char *str) {
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++) {
        char temp = str[i];
        str[i] = str[len - i - 1];
        str[len - i - 1] = temp;
    }
}

int sum_array(int *arr, int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}

void read_array(int *arr, int size, int index) {
    klee_print_expr("Reading from array at index", index);
    klee_print_expr("Value", arr[index]);
}

void copy_string(char *dest, const char *src, size_t max_len) {
    strncpy(dest, src, max_len - 1);
    dest[max_len - 1] = '\0';
}

int main() {
    char str[50] = "Hello, World!";
    reverse_string(str);

    int numbers[] = {1, 2, 3, 4, 5};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    sum_array(numbers, size);

    int index;
    klee_make_symbolic(&index, sizeof(index), "index");
    read_array(numbers, size, index);

    char dest[50];
    copy_string(dest, str, sizeof(dest));

    return 0;
}