#include <klee/klee.h>
#include <stdlib.h>

void process_data(int size) {
    int *array = (int *)malloc(size * sizeof(int));
    if (array == NULL) {
        return;
    }
    for (int i = 0; i < size; i++) {
        array[i] = i * 10;
    }
    klee_print_expr("First element:", array[0]);
    free(array);
}

int main() {
    int size;
    klee_make_symbolic(&size, sizeof(size), "size");
    if (size < 0) {
        return 1;
    }
    process_data(size);
    return 0;
}