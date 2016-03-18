#!/usr/bin/python

import os
import sys
import subprocess
import argparse
import fnmatch


# Get input: source directory of users guide.
def get_input():
    desc = 'Improve your file aesthetics by breaking long lines.'
    epilog = 'Script is made to check users-guide repository for long lines ' \
             'and break them if possible.'
    ap = argparse.ArgumentParser(description=desc, epilog=epilog)
    ap.add_argument('-m', '--maxlen',
                    help='the maximum length of a line (100 on default)',
                    type=int, default=100, metavar='LENGTH')
    ap.add_argument('-o', '--overwrite',
                    help='overwrites input .tex file(s)',
                    action='store_true')
    ap.add_argument('input', help='Print out a .tex file formatted '
                                  'or OVERWRITE a folder\'s .tex files.',
                    metavar='INPUT')

    return ap.parse_args()


# Check if a file contains long lines.
# Print out to stdout the affected lines' numbers.
def file_checker(content, maxlen):
    line_num = 1
    long_found = False

    for line in content:
        llen = len(line)
        if llen > maxlen:
            long_found = True
            print('Long line at %d' % line_num)
        line_num += 1

    if not long_found:
        print('There is no long lines in your file.')


# Checks a file's longest line.
# Returns with the number of chars of the longest line.
def dir_checker(content, maxlen):
    max_line_len = 0

    for line in content:
        llen = len(line)
        if (llen > max_line_len):
            max_line_len = llen

    return max_line_len


# Find .tex files in folder srcdir.
# Returns:
# * texfiles: list, contains the relative paths to .tex files.
def find_texfiles(srcdir):
    texfiles = []

    for root, directories, files in os.walk(srcdir):
        for file in fnmatch.filter(files, '*.tex'):
            texfiles.append(os.path.join(root, file))

    return texfiles


# Read file from file's path.
# Returns a list with the file's content.
def read_file(path):
    with open(path) as f:
        content = f.readlines()

    return content


# Output content(param 1) into file(param 2)
def dump(content, file):
    f = open(file, 'w')
    for line in content:
        f.write(line)
    f.close()


# Program logic when input argument is a directory.
def exec_dir(command, args):
    texfiles = find_texfiles(args.input)

    if args.overwrite:
        for file_name in texfiles:
            print('PROCESSING: %s' % file_name)
            content = subprocess.check_output(command + [file_name])
            dump(content, file_name)
        return 0

    for file_name in texfiles:
        content = read_file(file_name)
        max_line_len = dir_checker(content, args.maxlen)
        if args.maxlen < max_line_len:
            print("%s (%d)" % (file_name, max_line_len))


# Program logic when input argument is a file.
def exec_file(command, args):
    if args.overwrite:
        print('PROCESSING: %s' % args.input)
        command.append(args.input)
        content = subprocess.check_output(command)
        dump(content, args.input)
        return 0
    content = read_file(args.input)
    file_checker(content, args.maxlen)


# Function main() contains the program logic.
# Decides which functions should be called when
def main():
    args = get_input()

    if not os.path.exists(args.input):
        sys.stderr.write('ERROR: \'%s\' file or directory does not exists!\n'
                         'Use option -h for more information\n' % args.input)
        sys.exit(1)

    script_path = os.path.dirname(os.path.abspath(__file__))
    command = ['python']
    command.append(os.path.join(script_path, 'breaklines.py'))
    command.append(str(args.maxlen))

    # Input is a directory.
    if os.path.isdir(args.input):
        exec_dir(command, args)
        return 0

    # Input is a file.
    exec_file(command, args)


if __name__ == "__main__":
    main()
