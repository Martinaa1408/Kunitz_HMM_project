#!/bin/bash
# Extract the best hit per query from a BLAST or HMMER tabular output file

input_file=$1
output_file=$2

grep -v "^#" "$input_file" | sort -k1,1 -k5,5g | awk '!seen[$1]++' > "$output_file"

