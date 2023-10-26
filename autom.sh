#!/bin/bash

# Check if the user provided a text file as an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <input_text_file>"
    exit 1
fi

input_file="$1"

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "Input file '$input_file' not found."
    exit 1
fi

# Loop through each line in the input file
while IFS= read -r line; do
    if [ -n "$line" ]; then
        # Run the Python command with the line as a parameter
        python3 main.py -slimit 0.1 -gav "$line"

        # Wait for the process to finish
        wait
    fi
done < "$input_file"

echo "Processing complete."
