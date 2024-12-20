#include <klee/klee.h>
#include <stdint.h>

int calculate_discount(int price, int percentage) {
    if (percentage < 0 || percentage > 100) {
        return -1;
    }
    return (price * percentage) / 100;
}

int main() {
    int price, percentage;
    klee_make_symbolic(&price, sizeof(price), "price");
    klee_make_symbolic(&percentage, sizeof(percentage), "percentage");

    int discount = calculate_discount(price, percentage);

    if (discount < 0) {
        klee_print_expr("Invalid discount percentage.", discount);
    } else {
        int final_price = price - discount;
        klee_print_expr("Final price after discount:", final_price);
    }

    return 0;
}