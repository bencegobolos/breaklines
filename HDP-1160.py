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
    ap.add_argument('-c', '--check',
                    help='check if file or dir contains long lines',
                    action='store_true')
    ap.add_argument('input', help='Print out a .tex file formatted '
                                  'or OVERWRITE a folder\'s .tex files.',
                    metavar='INPUT')
    try:
        return ap.parse_args()

    except:
        ap.print_help()
        sys.exit(-1)


# Check if a file contains long lines.
# Print out to stdout the affected lines' numbers.
def file_checker(content, maxlen):
    line_num = 1
    long_found = False

    for line in content:
        llen = len(line)
        if llen > maxlen:
            long_found = True
            print('***\t' + 'LONG LINE on line ' + str(line_num))
        line_num += 1

    if not long_found:
        print('[!]\t' + 'There is no long lines in your file.')


# Checks a file's longest line.
# Returns with the number of chars of the longest line.
def dir_checker(content, maxlen):
    maxllen = 0

    for line in content:
        llen = len(line)
        if (llen > maxllen):
            maxllen = llen

    return maxllen


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


# If first input is a directory
# ask user to confirm to overwrite every .tex file.
# Returns:
# * 'True', if user_input is 'yes'
# * 'False' otherwise.
def confirm_srcdir():
    execute = False

    print('WARNING: This command will overwrite every .tex file in your directory')
    user_input = str(raw_input('Continue? [yes/NO]: '))
    if user_input == 'yes':
        execute = True

    return execute


def main():
    args = get_input()

    script_path = os.path.dirname(os.path.abspath(__file__))
    command = ['python']
    command.append(os.path.join(script_path, 'breaklines.py'))
    command.append(str(args.maxlen))

    # Input is a directory.
    if os.path.isdir(args.input):
        texfiles = find_texfiles(args.input)

        if args.check:
            for file in texfiles:
                content = read_file(file)
                maxllen = dir_checker(content, args.maxlen)
                if args.maxlen < maxllen:
                    print(file)
                    print("\tMax length: " + str(maxllen) + '\n')
            sys.exit(0)

        # Confirm if user wants to overwrite .tex files.
        execute = confirm_srcdir()
        if not execute:
            print('Script aborted.')
            sys.exit(-1)

        for file in texfiles:
            command.append(file)
            content = subprocess.check_output(command)
            command.pop()
            dump(content, file)
        sys.exit(0)

    # Input is a file.
    elif os.path.isfile(args.input):
        if args.check:
            content = read_file(args.input)
            file_checker(content, args.maxlen)
            sys.exit(0)
        command.append(args.input)
        subprocess.call(command)
        sys.exit(0)

    print('\nScript is made to check users-guide repository for long lines.')
    print('Use -h or --help option to get more info.\n')
    sys.exit(-1)


if __name__ == "__main__":
    main()
