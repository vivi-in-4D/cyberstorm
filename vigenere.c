// team: parasauras
// date: 3/24/2023
// description: cyen 301 program 2, implements vigenere cypher


#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <limits.h>



// it is important to note, we take in unsigned chars because if we don't, c will consider chars like 'ç', which should have a value of 135, to have a negative value of 121, which breaks character wrapping... thanks chatGPT ;)
char cypher(unsigned char input, unsigned char key, bool encrypt_mode) {
    char lower_or_upper_case_val = 'a';



    // key case value does not matter, so if we are uppercase, swap to lower, thats what the math in this function is built for
    if (key  >= 65 && key <= 90) {
        key += 32;
    }
    // if key is not a letter, don't do anything, it is not specified what we do in this case in the assignment, this is my solution
    else if (!(key  >= 97 && key <= 122)) {
        return input;
    }



    // we need to figure out what to compare our char to in order to see if we need to wrap
    if (input  >= 97 && input <= 122) {
        lower_or_upper_case_val = 'a';
    }
    else if (input  >= 65 && input <= 90) {
        lower_or_upper_case_val = 'A';
    }
    else {
        return input;
    }



    // encrypt mode
    if (encrypt_mode) {
        input += key - 'a';

        // wrapping
        if (input > (lower_or_upper_case_val + 25)) {
            input -= 26;
        }
    }
    // decrypt mode
    else {
        input -= key - 'a';

        // wrapping
        if (input < lower_or_upper_case_val) {
            input += 26;
        }
    }



    return input;
}



// since we are doing string related functions and using string indexes, we cannot just pass a char** type, we have to pass a whole string, this is why I don't have another function calling this one, which would make the code in our main loop look better, as we do not have to repeat ourselves and we can call it without passing a constant
int skip_spaces(char key_str[], int index, int depth) {
    if (depth > strlen(key_str)) {
        return INT_MIN; // if we get this value, our final count will be less than 0 unless our key is larger than the max int value - 1, we use this to determine whether or not we end the program right now due to a key full of spaces
    }



    // if char in key is a space, recursive call
    if (key_str[index % strlen(key_str)] == ' ') {
        return 1 + skip_spaces(key_str, index+1, depth+1);    // calls itself, incrementing index and depth
    }



    return 0;   // if not a space we break from recursion
}



int main(int argc, char* argv[]) {
    bool encrypt_mode;
    char str_to_cypher[400]; // I was having a lot of issues with dynamically allocating memory, so I just made the size of our string really high, not a great solution, but it is functional
    int space_count;    // space_count counts the amount of spaces we've had on each run of our main for loop, it ensures we are at the correct position in our key, and prevents us from having to copy the entire key without spaces, as well as store an entire string for that new key,
    int temp;   // temporarily stores data from skip_spaces function, so we can range check


    // if we dont have enough arguments
    if (argc < 3) {
        printf("please provide proper usage\ne.g. ./vigenere [option] [key]\n");
        return -1;
    }



    // checks mode
    if (!strcmp(argv[1], "-d")) {
        encrypt_mode = false;   // decrypt mode
    }
    else if (!strcmp(argv[1], "-e")) {
        encrypt_mode = true;    //encrypt mode
    }
    // if not -e or -d
    else {
        printf("Please select one of the following options: -e [encrypt] or -d [decrypt]\ne.g. usage: ./vigenere -d hello\n");
        return -2;
    }



    // main loop
    for (;;) {
        space_count = 0;    // at the start of the main loop set the count for the amount of spaces in our key back to 0

        scanf(" %[^\n]s[^\n]", str_to_cypher);  // get user input without newline char at the end or spaces at the beginning, and including spaces in the middle



        for (int i=0; i<strlen(str_to_cypher); i++) {
            temp = skip_spaces(argv[2], i + space_count, 0);

            if (temp < 0) {
                printf("please enter a key that contains more than just spaces\n"); // if key entered was just spaces, early exit
                return -3;
            }

            space_count += temp;



            // if we encounter a space in the input, we want to skip it, this is the easiest way I could think of
            if (str_to_cypher[i] == ' ') {
                space_count--;
                continue;
            }



            str_to_cypher[i] = cypher(str_to_cypher[i], argv[2][(i + space_count) % strlen(argv[2])], encrypt_mode);  // for every char in str_to_cypher, we encrypt/decrypt that char and store it in str_to_cypher
        }



        str_to_cypher[strlen(str_to_cypher)] = '\0';  // prevents us from having to clear str_to_cypher every time we get a new input, and prevents random characters appearing at the end of strings due to buffer overflow

        printf("%s\n", str_to_cypher);
    }



    return 1;
}