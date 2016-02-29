#!/usr/bin/python

import re
import os
import sys
import fnmatch

# How many characters allowed in one line?
breakpoint = 100
brackets = 0
cmd = 0

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
  for line in content:
    newline = splitLine(line)
    formatted.extend(newline)

  return formatted


# Insert newlines into long lines.
def splitLine(line):
  processed = []
  isComment = 0
  global brackets
  global cmd

  # Do not break line if represents a (partial) code.
  if (re.match("(.*)begin{cmd}(.*)", line)):
    cmd -= 1

  if (re.match("(.*)\\end{cmd}(.*)", line)):
    cmd += 1

  if (re.match("(.*)begin{code}(.*)", line)):
    cmd -= 1

  if (re.match("(.*)\\end{code}(.*)", line)):
    cmd += 1

  # Is line longer then breakpoint?
  llen = len(line)
  if (llen >= breakpoint):
    idx = 0
    save = 0

    # Search for insertion points
    while(idx < llen):
      checkbrackets(line[idx])

      if (isInsertionPossible(line[idx]) and cmd == 0):
        save = idx

      # if { bracket is \hint{, do not mind it.
      if (line[idx-5:idx] == '\hint'):
        brackets += 1

      if (line[idx-5:idx] == '\samp'):
        brackets += 1

      # Found a \hint or \samp closing '}' bracket.
      if (brackets > 0):
        brackets -= 1

      # If line is comment, break it and insert %.
      if (line[idx] == '%' and line[idx-1] != '\\'):
        isComment = 1

      idx += 1

      # Found an insertion point.
      if (save > 0 and idx >= breakpoint):
        brackets = 0
        processed.extend(line[:save])
        processed.extend('\n')
        if (isComment):
          processed.extend(splitLine('%' + line[save+1:]))
        else:
          processed.extend(splitLine(line[save+1:]))
        return processed

    # If can't insert \n before 100th char
    brackets = 0
    return line

  else:
    processed.extend(line)

  return processed


# Check if character is a curly bracket.
def checkbrackets(c):
  global brackets

  if (c == '{'):
    brackets -= 1
  elif (c == '}'):
    brackets += 1
  else:
    return 0


# Check if we can insert \n at current character.
def isInsertionPossible(c):
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
