#include <stdio.h>
#include <time.h>

// GPT-4o

int main() {
    // Record start time
    clock_t start = clock();

    // Perform the summation
    long long result = 0; // Use long long for large numbers
    for (int i = 1; i < 10000000; i++) {
        result += i;
    }

    // Record end time
    clock_t end = clock();

    // Calculate elapsed time in seconds
    double elapsed = (double)(end - start) / CLOCKS_PER_SEC;

    // Print the result and elapsed time
    // printf("\x1b[1;42;90mC: %lld in %.6f seconds\x1b[0m.\n", result, elapsed);
    printf("\x1b[1;42;90mC: in %.6f seconds\x1b[0m.\n", elapsed);

    return 0;
}
