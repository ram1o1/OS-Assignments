#!/bin/bash

while true
do
    echo "1 Area of a Circle"
    echo "2 Circumference of a Circle"
    echo "3 Area of a Rectangle"
    echo "4 Area of a Square"
    echo "5 Exit"
    read -p "Enter your choice: " ch

    case $ch in
        1)
            read -p "Enter radius: " r
            ans=$(echo "3.14 * $r * $r" | bc)
            echo "Area of Circle = $ans"
            ;;
        2)
            read -p "Enter radius: " r
            ans=$(echo "2 * 3.14 * $r" | bc)
            echo "Circumference of Circle = $ans"
            ;;
        3)
            read -p "Enter length: " l
            read -p "Enter breadth: " b
            ans=$(echo "$l * $b" | bc)
            echo "Area of Rectangle = $ans"
            ;;
        4)
            read -p "Enter side: " s
            ans=$(echo "$s * $s" | bc)
            echo "Area of Square = $ans"
            ;;
        5)
            exit 0
            ;;
        *)
            echo "Wrong choice!"
            ;;
    esac
    echo ""
done