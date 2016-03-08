#!/usr/bin/python

import re
import sys

# How many characters allowed in one line?
maxlen = 99

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
  llen = remain_len = len(line)

  # Short line, ignore it.
  if llen <= maxlen:
    return line

  # Long line
  processed = []
  save = 0
  num_of_indents = check_indentation(line)
  indentation = ' ' * num_of_indents
  comment = is_comment(line)

  # Search for insertion points
  while remain_len > maxlen:
    idx = tmp_save = brackets = 0

    while idx < remain_len:
      brackets += check_brackets(line[save + idx])
      brackets += check_exception(line, idx, brackets)

      if is_insertion_possible(line[save + idx], brackets):
        tmp_save = save + idx

      if tmp_save > num_of_indents and idx >= maxlen:
        if save != 0:
          processed.extend(indentation)
        processed.extend(line[save:tmp_save])
        processed.extend('\n')
        if 0 <= comment <= save + tmp_save:
          processed.extend('%')
        save = tmp_save + 1
        remain_len = len(line[save:])
        break
      idx += 1
    if tmp_save <= num_of_indents:
      if save != 0:
        processed.extend(indentation)
      processed.extend(line[save:tmp_save])
      break
  # Remaining
  if save != 0:
    processed.extend(indentation)
  processed.extend(line[save:])

  return processed


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


# Check indentation of a line
# Returns a number: number of spaces(' ').
def check_indentation(line):
  idx = 0
  while (line[idx] == ' '):
    idx += 1

  return idx


# Search for comment in line.
# Returns an idx, where line becomes being a comment.
# Returns -1 if line is not comment.
def is_comment(line):
  res = -1
  idx = 0
  llen = len(line)
  while idx < llen:
    if line[idx] == '%' and line[idx-1] != '\\':
      res = idx
      break
    idx += 1

  return res

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
