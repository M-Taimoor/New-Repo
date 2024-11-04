// Filename: add_numbers.c
#include <stdio.h>

// Function to add two numbers
int add(int a, int b) {
    return a + b;
}

// Compile this C code into a shared library (on Windows, the output will be add_numbers.dll)
// gcc -shared -o add_numbers.dll add_numbers.c