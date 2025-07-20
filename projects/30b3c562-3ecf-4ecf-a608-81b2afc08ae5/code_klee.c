#include <stdlib.h>
#include <string.h>
#include <klee/klee.h>

int main() {
    char *str[1] = {(char *)NULL};
    if ((str[0] = (char *)malloc(256 * sizeof(char))) != NULL) {
        strcpy(str[0], "Falut!");
        str[0][0] = 'S';
        free(str[0]);
        char *str1 = malloc(65536);
        free(str1);
        str[0][0] = 'S';
    }
    return 0;
}