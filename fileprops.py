#!/usr/bin/python

import re
import os
import sys
import fnmatch


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
  with open(texfile) as f:
    content = f.readlines()

  return content


def maxLength(content):
  maxlen = 0

  for line in content:
    llen = len(line)
    if (llen > maxlen):
      maxlen = llen

  return maxlen


#### START PROGRAM ####
def main():
  srcdir = getInput()
  files = find(srcdir)
#DEBUG
#  content = readfile(files[14])
#  newfile = insertNewLines(content)
#  dump(newfile, 'out.txt')
#DEBUG
  for file in files:
    content = readfile(file)
    maxlen = maxLength(content)
    print(file)
    print("Max length: " + str(maxlen))
      
  print("PROGRAM ENDS.")


if __name__ == "__main__":
  main()
