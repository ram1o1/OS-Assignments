#!/bin/bash

today=$(date +%Y-%m-%d)

for file in *.jpg
do
    if [ -f "$file" ]; then
        mv "$file" "$today-$file"
    fi
done