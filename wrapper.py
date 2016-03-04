#!/usr/bin/python

import re
import os
import sys
import fnmatch
import breaklines

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


# DEBUG: output content(param 1) into file(param 2)
def dump(content, file):
  f = open(file, 'w')
  for line in content:
    f.write(line)
  f.close()


#### START PROGRAM ####
def main():
  srcdir = get_input()
  files = find(srcdir)
  for file in files:
    print('Processing file: ' + file)
    content = breaklines.read_file(file)
    newfile = breaklines.format_file(content)
    dump(newfile, file)
    print('Formatted file: ' + file)
  print("PROGRAM ENDS.")


if __name__ == "__main__":
  main()
