#include <stdio.h>
#include <stdint.h>

int calculate_discount(int price, int percentage) {
    if (percentage < 0 || percentage > 100) {
        return -1; // Invalid percentage
    }
    return (price * percentage) / 100; // Potential overflow
}

int main() {
    int price, percentage;

    printf("Enter price: ");
    scanf("%d", &price);

    printf("Enter discount percentage: ");
    scanf("%d", &percentage);

    int discount = calculate_discount(price, percentage);

    if (discount < 0) {
        printf("Invalid discount percentage.\n");
    } else {
        int final_price = price - discount; // Subtle overflow possibility here
        printf("Final price after discount: %d\n", final_price);
    }

    return 0;
}

