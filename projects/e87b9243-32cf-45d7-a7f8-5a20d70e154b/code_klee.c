#include <stdlib.h>
#include <string.h>
#include <klee/klee.h>

unsigned int getRand() {
    unsigned int r;
    klee_make_symbolic(&r, sizeof(r), "r");
    return r;
}

char *rand_text() {
    unsigned length = getRand() % 50 - 1;
    char *t = malloc((length + 1) * sizeof(char));
    if (!t) 
        return NULL;
    unsigned i = 0;
    for (; i < length; ++i) {
        t[i] = (char)((getRand() % 26) + 'a');
    }
    t[i] = '\0';
    return t;
}

int main() {
    char *buf = (char *)NULL;
    buf = malloc(25 * sizeof(char));
    
    if (buf != (char *)NULL) {
        char *t = rand_text();
        if (t) {
            strcpy(buf, t);
            free(t);
        }
        free(buf);
    }
    return 0;
}