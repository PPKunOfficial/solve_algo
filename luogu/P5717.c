#include <stdio.h>

void swap(int* x, int* y) {
    int temp = *x;
    *x = *y;
    *y = temp;
}

int main() {
    int a, b, c;
    scanf("%d %d %d", &a, &b, &c);

    if (a > b)
        swap(&a, &b);
    if (b > c)
        swap(&b, &c);
    if (a > b)
        swap(&a, &b);

    if (a + b <= c) {
        printf("Not triangle\n");
        return 0;
    }

    int angle_type = (a * a + b * b == c * c)  ? 1
                     : (a * a + b * b > c * c) ? 2
                                               : 3;

    switch (angle_type) {
        case 1:
            printf("Right triangle\n");
            break;
        case 2:
            printf("Acute triangle\n");
            break;
        case 3:
            printf("Obtuse triangle\n");
            break;
    }

    if (a == b || b == c) {
        printf("Isosceles triangle\n");
    }

    if (a == b && b == c) {
        printf("Equilateral triangle\n");
    }

    return 0;
}