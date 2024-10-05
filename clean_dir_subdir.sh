#!/bin/bash

# Check if a directory is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Get the directory from the first argument
DIRECTORY="$1"

# Check if the provided argument is a directory
if [ ! -d "$DIRECTORY" ]; then
    echo "Error: $DIRECTORY is not a valid directory."
    exit 1
fi

# Find and delete files in the specified directory and its subdirectories
find "$DIRECTORY" -type f -exec rm -f {} +

echo "All files within $DIRECTORY and its subdirectories have been deleted."
