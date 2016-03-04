#!/usr/bin/python

import re
import os
import sys
import fnmatch

# How many characters allowed in one line?
breakpoint = 100

# Get input: source directory of users guide.
def getInput():
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
def readfile(texfile):
  print("Reading file: " + texfile)
  with open(texfile) as f:
    content = f.readlines()

  return content


# Build new file.
def insertNewLines(content):
  print("Processing...")

  # processed will contain the formatted tex file
  formatted = []
  cmd = 0

  for line in content:
    cmd += checkcode(line)
    if (cmd == 0):
      newline = splitLine(line)
      formatted.extend(newline)
    else:
      formatted.extend(line)

  return formatted


# Insert newlines into long lines.
def splitLine(line):
  llen = len(line)

  # Long line
  if (llen >= breakpoint):
    # Initializing variables.
    processed = []
    idx = save = brackets = isComment = 0

    # Search for insertion points
    while(idx < llen):
      brackets += checkbrackets(line[idx])
      brackets += checkexception(line, idx, brackets)
      isComment = checkcomment(line, idx)

      if (isInsertionPossible(line[idx], brackets)):
        save = idx

      idx += 1

      # Found an insertion point (before or after breakpoint)
      if (save > 0 and idx >= breakpoint):
        processed.extend(line[:save])
        processed.extend('\n')
        if (isComment):
          processed.extend(splitLine('%' + line[save+1:]))
        else:
          processed.extend(splitLine(line[save+1:]))
        return processed

    # No insertion point found
    return line

  # Short line
  else:
    return line


# Check if character is a curly bracket.
def checkbrackets(c):
  if (c == '{'):
    return -1
  elif (c == '}'):
    return 1
  else:
    return 0


# Do not break line if represents a (partial) code.
def checkcode(line):
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
def checkexception(line, idx, brackets):
  if (line[idx-5:idx] == '\hint'):
    return 1
  if (line[idx-5:idx] == '\samp'):
    return 1
 
 # Found a \hint or \samp closing '}' bracket.
  if (brackets > 0):
    return -1

  return 0


# If line is comment, break it and insert %.
def checkcomment(line, idx):
  if (line[idx] == '%' and line[idx-1] != '\\'):
    return 1
  else:
    return 0


# Check if we can insert \n at current character.
def isInsertionPossible(c, brackets):
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
  srcdir = getInput()
  files = find(srcdir)
  for file in files:
    content = readfile(file)
    newfile = insertNewLines(content)
    dump(newfile, file)  
  print("PROGRAM ENDS.")


if __name__ == "__main__":
  main()
