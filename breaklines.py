#!/usr/bin/python

import re
import os
import sys
import fnmatch

# How many characters allowed in one line?
maxlen = 100

# Get input: source directory of users guide.
def get_input():
  if len(sys.argv) < 2:
    print("ERROR: One argument reqired: .tex file.")
    sys.exit(0)
  else:
    return str(sys.argv[1])


# Read .tex file.
def read_file(texfile):
  with open(texfile) as f:
    content = f.readlines()

  return content


# Build new file.
def format_file(content):

  # Var formatted will contain the formatted tex file.
  formatted = []
  # Do not insert newline char in code!
  cmd = 0

  for line in content:
    cmd += check_code(line)
    if cmd == 0:
      newline = split_line(line)
      formatted.extend(newline)
    else:
      formatted.extend(line)

  return formatted


# Insert newlines into long lines.
def split_line(line):
  llen = len(line)

  # Long line
  if llen <= maxlen:
    return line

  # Initializing variables.
  processed = []
  idx = save = brackets = 0

  # Search for insertion points
  while idx < llen:
    brackets += check_brackets(line[idx])
    brackets += check_exception(line, idx, brackets)

    if (is_insertion_possible(line[idx], brackets)):
      save = idx

    idx += 1

    # Found an insertion point (before or after maxlen)
    if save > 0 and idx >= maxlen:
      processed.extend(line[:save])
      processed.extend('\n')
      if is_comment(line, idx):
        processed.extend(split_line('%' + line[save+1:]))
      else:
        processed.extend(split_line(line[save+1:]))
      return processed

  # No insertion found
  return line


# Check if character is a curly bracket.
def check_brackets(c):
  if c == '{':
    return -1
  elif c == '}':
    return 1
  else:
    return 0


# Do not break line if represents a (partial) code.
def check_code(line):
  if re.match("(.*)\\\\begin{cmd}(.*)", line):
    return -1
  if re.match("(.*)\\\\end{cmd}(.*)", line):
    return 1
  if re.match("(.*)\\\\begin{code}(.*)", line):
    return -1
  if re.match("(.*)\\\\end{code}(.*)", line):
    return 1

  return 0


# if { bracket is \hint{, do not mind it.
def check_exception(line, idx, brackets):
  if line[idx-5:idx] == '\hint':
    return 1
  if line[idx-5:idx] == '\samp':
    return 1
 
 # Found a \hint or \samp closing '}' bracket.
  if brackets > 0:
    return -1

  return 0


# If line is comment, break it and insert %.
def is_comment(line, idx):
  return line[idx] == '%' and line[idx-1] != '\\'

# Check if we can insert \n at current character.
def is_insertion_possible(c, brackets):
  return c == ' ' and brackets == 0


# DEBUG: output content(param 1) into file(param 2)
def dump(content):
  print(''.join(content))


#### START PROGRAM ####
def main():
  file = get_input()
  content = read_file(file)
  newfile = format_file(content)
  dump(newfile)


if __name__ == "__main__":
  main()
