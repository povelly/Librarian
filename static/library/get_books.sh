#!/bin/bash

book_id=100
count=0
while [ "$count" -lt 2000 ]
do
    URL="http://www.gutenberg.org/files/$book_id/$book_id-0.txt"
    CURL=$(curl $URL -o "$book_id.txt" --fail  2>&1)

    if [ $? -ne 0 ] 
    then
        echo "$book_id not found"
    else
        count=$((count + 1))
    fi
    book_id=$((book_id + 1))
done