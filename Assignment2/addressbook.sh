#!/usr/bin/bash

FILE="address_book.txt"

while true; do
    echo "1 Create Address Book"
    echo "2 View Address Book"
    echo "3 Insert a Record"
    echo "4 Delete a Record"
    echo "5 Modify a Record"
    echo "6 Exit"
    read -p "Enter your choice: " choice

    case $choice in
        1)
            touch "$FILE"
            echo "Address Book created."
            ;;
        2)
            if [ -s "$FILE" ]; then
                echo "Name | Phone | Email"
                cat "$FILE"
            else
                echo "Address Book is empty."
            fi
            ;;
        3)
            read -p "Enter Name: " name
            read -p "Enter Phone: " phone
            read -p "Enter Email: " email
            echo "$name | $phone | $email" >> "$FILE"
            echo "Record inserted."
            ;;
        4)
            read -p "Enter Name to delete: " search
            if grep -iq "$search" "$FILE"; then
                grep -iv "$search" "$FILE" > temp.txt
                mv temp.txt "$FILE"
                echo "Record deleted."
            else
                echo "Record not found."
            fi
            ;;
        5)
            read -p "Enter Name of the record to modify: " search
            if grep -iq "$search" "$FILE"; then
                grep -iv "$search" "$FILE" > temp.txt
                mv temp.txt "$FILE"
                read -p "Enter new Name: " name
                read -p "Enter new Phone: " phone
                read -p "Enter new Email: " email
                echo "$name | $phone | $email" >> "$FILE"
                echo "Record modified."
            else
                echo "Record not found."
            fi
            ;;
        6)
            exit 0
            ;;
        *)
            echo "Invalid choice."
            ;;
    esac
    echo ""
done