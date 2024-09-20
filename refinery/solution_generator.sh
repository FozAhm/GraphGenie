#!/bin/bash

# Check if the directory is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 /path/to/your/folder"
    exit 1
fi

# Directory to scan for files
directory="$1"
echo $directory

# Command to execute for each file
command="docker run -it --rm --cpus 4 -v $directory:/data ghcr.io/graphs4value/refinery-cli:latest generate"

# Input variables
input1="-r 1"
input2="-r 2"
input3="-r 3"
input4="-r 4"

# Loop through each file in the directory
for file in "$directory"/*; do
    if [[ -f "$file" ]]; then
        echo "Processing file: $file"

        # Extract the file name without the extension
        filename=$(basename -- "$file")
        filename_without_extension="${filename%.*}"
        
        # Execute the command three times with different input variables
        cmd1="$command $filename -o ${filename_without_extension}R1.solution $input1"
        echo "Executing: $cmd1"
        eval $cmd1
        cmd2="$command $filename -o ${filename_without_extension}R2.solution $input2"
        echo "Executing: $cmd2"
        eval $cmd2
        cmd3="$command $filename -o ${filename_without_extension}R3.solution $input3"
        echo "Executing: $cmd3"
        eval $cmd3
        cmd4="$command $filename -o ${filename_without_extension}R4.solution $input4"
        echo "Executing: $cmd4"
        eval $cmd4
    fi
done
