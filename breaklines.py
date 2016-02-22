#!/usr/bin/python

import re
import os
import sys
import fnmatch

# How many characters allowed in one line?
breakpoint = 100
brackets = 0

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


# Process line (insert '\n') with logic like this
# * must be inserted before the line 100th character
# * insert it at the least distance from 100th char as possible
# * insert it at the character ' ' (space)
# * cannot be inserted before { } brackets.
# * if examined char is '\n' then continue
def insertNewLines(content):
  print("Processing...")

  # processed will contain the formatted tex file
  formatted = []
  for line in content:
    newline = splitLine(line)
    formatted.extend(newline)

  return formatted

def splitLine(line):
  processed = []

  llen = len(line)
  if (llen >= breakpoint):
    idx = 0
    save = 0

    while(save < breakpoint and idx < llen):
      checkbrackets(line[idx])
      if (isInsertionPossible(line[idx])):
        save = idx
      idx += 1

      if (save >= breakpoint):
        processed.extend(line[:save])
        processed.extend('\n')
        if (len(line[save+1:]) >= breakpoint):
          processed.extend(splitLine(line[save+1:]))
          return processed
        else:
          processed.extend(line[save+1:])
          return processed

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


# Filter out hint lines.
def isHint(line):
  if (line[0:5] = '\hint{'):
    return 1
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
  print("Formatting done.")


if __name__ == "__main__":
  main()
