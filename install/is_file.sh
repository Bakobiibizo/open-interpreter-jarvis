#!/bin/bash

# Check if the correct number of arguments were passed
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 filename url"
    exit 1
fi

# The name of the file you want to check for is the first argument
FILENAME="$1"

# The URL from where you want to download the file is the second argument
URL="$2"

# Check if the file exists
if [ ! -f "$FILENAME" ]; then
    # If the file doesn't exist, download it
    echo "File not found. Downloading..."
    wget "$URL" -O "$FILENAME" -q
    # OR you can use curl if wget isn't available:
    # curl -o "$FILENAME" "$URL"
else
    echo "File already exists."
fi
