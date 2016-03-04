#!/usr/bin/python

import re
import os
import sys
import fnmatch

# How many characters allowed in one line?
breakpoint = 100

# Get input: source directory of users guide.
def get_input():
  if (len(sys.argv) < 2):
    print("ERROR: One argument reqired: srcdir of users guide.")
    sys.exit(0)

  else:
    return str(sys.argv[1])


# Find .tex files in root folder.
def find(srcdir):
  texfiles = []
  for root, directories, files in os.walk(srcdir):
    for file in fnmatch.filter(files, '*.tex'):
      texfiles.append(os.path.join(root, file))

  return texfiles


# Read .tex file.
def read_file(texfile):
  print("Reading file: " + texfile)
  with open(texfile) as f:
    content = f.readlines()

  return content


# Build new file.
def format_file(content):
  print("Processing...")

  # Var formatted will contain the formatted tex file.
  formatted = []
  # Do not insert newline char in code!
  cmd = 0

  for line in content:
    cmd += check_code(line)
    if (cmd == 0):
      newline = split_line(line)
      formatted.extend(newline)
    else:
      formatted.extend(line)

  return formatted


# Insert newlines into long lines.
def split_line(line):
  llen = len(line)

  # Long line
  if (llen >= breakpoint):
    # Initializing variables.
    processed = []
    idx = save = brackets = is_comment = 0

    # Search for insertion points
    while(idx < llen):
      brackets += check_brackets(line[idx])
      brackets += check_exception(line, idx, brackets)
      is_comment = check_comment(line, idx)

      if (is_insertion_possible(line[idx], brackets)):
        save = idx

      idx += 1

      # Found an insertion point (before or after breakpoint)
      if (save > 0 and idx >= breakpoint):
        processed.extend(line[:save])
        processed.extend('\n')
        if (is_comment):
          processed.extend(split_line('%' + line[save+1:]))
        else:
          processed.extend(split_line(line[save+1:]))
        return processed

  # Short line or no insertion found
  return line


# Check if character is a curly bracket.
def check_brackets(c):
  if (c == '{'):
    return -1
  elif (c == '}'):
    return 1
  else:
    return 0


# Do not break line if represents a (partial) code.
def check_code(line):
  if (re.match("(.*)begin{cmd}(.*)", line)):
    return -1
  if (re.match("(.*)\\end{cmd}(.*)", line)):
    return 1
  if (re.match("(.*)begin{code}(.*)", line)):
    return -1
  if (re.match("(.*)\\end{code}(.*)", line)):
    return 1

  return 0


# if { bracket is \hint{, do not mind it.
def check_exception(line, idx, brackets):
  if (line[idx-5:idx] == '\hint'):
    return 1
  if (line[idx-5:idx] == '\samp'):
    return 1
 
 # Found a \hint or \samp closing '}' bracket.
  if (brackets > 0):
    return -1

  return 0


# If line is comment, break it and insert %.
def check_comment(line, idx):
  if (line[idx] == '%' and line[idx-1] != '\\'):
    return 1
  else:
    return 0


# Check if we can insert \n at current character.
def is_insertion_possible(c, brackets):
  if (c == ' ' and brackets == 0):
    return 1
  else:
    return 0


# DEBUG: output content(param 1) into file(param 2)
def dump(content, file):
  f = open(file, 'w')
  for line in content:
    f.write(line)
  f.close()
  print("Formatted file: " + file)


#### START PROGRAM ####
def main():
  srcdir = get_input()
  files = find(srcdir)
  for file in files:
    content = read_file(file)
    newfile = format_file(content)
    dump(newfile, file)  
  print("PROGRAM ENDS.")


if __name__ == "__main__":
  main()
