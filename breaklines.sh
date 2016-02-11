#!/bin/bash

# Break lines at max_width
max_width=100

if (( $# != 1  )); then
  echo "One argument required: root folder of users guide."
  exit
fi

# Find all the .tex files
texfiles=(`find $1 -name *.tex`)

# Iterate over .tex files
for file in ${texfiles[@]}
do

  echo "Examine file: $file"

  # Read current file
  readarray current_file < $file
  current_width=${#current_file}

  # Iterate over lines
  for lines in $current_file
  do

    # Braces: 0 when occurences of '{' or '[' are equal to the
    # occurences of '}' or ']'.
    #
    # Opening brace: +1
    # Closing brace: -1
    braces=0

    # Iterate over characters
    for (( i=0; i<current_width; i++ ));
    do
      # Select where this script should break a line
      # Ex1: do not break between {} or []

      echo ${current_file:i:1}
    done
  done
done
