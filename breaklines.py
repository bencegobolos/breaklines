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


# Process lines: if "len(line) > 100" insert "\n" somehow.
def insertBreak(content):
  print("Processing...")
  processed = []
  for line in content:
    numOfInsert = len(line)/breakpoint
    countInsert = 0

    if (numOfInsert >= 1):
      while(countInsert <= numOfInsert):
        newLine = line[breakpoint*countInsert-countInsert:breakpoint*(countInsert+1)-(countInsert+1)]
        processed.extend(newLine)
        processed.extend('\n')
        countInsert = countInsert + 1
    else:
      processed.extend(line)
  return processed


# DEBUG: output content(param 1) into file(param 2)
def dump(content, file):
  f = open(file, 'w')
  for line in content:
    f.write(line)
  f.close()


#### START PROGRAM ####
def main():
  srcdir = getInput()
  files = find(srcdir)
  i = 1
  for file in files:
    content = readfile(file)
    proc = insertBreak(content)
    dump(proc, str(i) + ".txt")
    i = i + 1

if __name__ == "__main__":
  main()
