#!/usr/bin/bash
echo "Give me a number, I will calculate the factorial of that number: "
read given_num

# first we check if the given number is +ve -ve or Zero
# then after use for loop to claculate factorial if it is +ve and print
# print 1 if it is 0 
# print we cannot calculate factorial if the give number is -ve
if [ $given_num -gt 0 ]; then
    fact=1
    temp_num=$given_num
    
    while [ $temp_num -gt 1 ]; do
        fact=$((fact * temp_num))
        temp_num=$((temp_num - 1))
    done
    
    echo "The factorial of the given number $given_num is: $fact"

elif [ $given_num -eq 0 ]; then
    echo "The factorial of 0 is: 1"

elif [ $given_num -lt 0 ]; then
    echo "The number is negative; cannot calculate factorial."
fi