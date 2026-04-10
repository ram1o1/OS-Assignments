#include <stdio.h>

// Each level multiplies the previous by 10
#define M1(a) a, a, a, a, a, a, a, a, a, a
#define M2(a) M1(a), M1(a), M1(a), M1(a), M1(a), M1(a), M1(a), M1(a), M1(a), M1(a)
#define M3(a) M2(a), M2(a), M2(a), M2(a), M2(a), M2(a), M2(a), M2(a), M2(a), M2(a)
#define M4(a) M3(a), M3(a), M3(a), M3(a), M3(a), M3(a), M3(a), M3(a), M3(a), M3(a)
#define M5(a) M4(a), M4(a), M4(a), M4(a), M4(a), M4(a), M4(a), M4(a), M4(a), M4(a)

int main() {
    // M5(1) expands to 100,000 integers
    int data[] = { M5(1) };
    
    int sum = 0;
    for(int i = 0; i < 100000; i++) {
        sum += data[i];
    }
    
    printf("Sum: %d\n", sum);
    return 0;
}
