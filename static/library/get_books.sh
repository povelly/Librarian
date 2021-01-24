#!/bin/bash

CURL_BASE_COMMAND="curl http://www.gutenberg.org/files/"

for i in {5000..7000}
do 
    CURL_FULL_COMMAND="$CURL_BASE_COMMAND$i/$i-0.txt -o \"$i.txt\""
    eval $CURL_FULL_COMMAND
done