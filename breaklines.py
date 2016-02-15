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
  print("Reading file: " + texfile)
  with open(texfile) as f:
    content = f.readlines()

  return content


# Process lines: if "len(line) > 100" insert "\n" somehow.
def insertBreak(content):
  processed = []
  for line in content:
    if (len(line) > 100):
      # FAIL!!!
      processed.extend(line[:100] + "\n")
      processed.extend(line[102:])
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
  content = readfile(files[33])
  proc = insertBreak(content)
  dump(proc, "out.txt")

if __name__ == "__main__":
  main()
