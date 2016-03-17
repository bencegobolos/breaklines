#!/usr/bin/python

import os
import sys
import subprocess
import argparse
import fnmatch

# Get input: source directory of users guide.
def get_input():
    desc = 'Improve your file aesthetics by breaking long lines.'
    ap = argparse.ArgumentParser(description=desc)
    ap.add_argument('-m', '--maxlen', help='the maximum length of a line '
                                           '(100 on default)',
                    type=int, default=100, metavar='LENGTH')
    group = ap.add_mutually_exclusive_group()
    group.add_argument('--srcdir', help='OVERWRITES users-guide repo .tex files')
    group.add_argument('-f', '--file', help='the .tex file you want to print out formatted',
                    type=file, metavar='TEXFILE')
    group.add_argument('-c', '--check', help='check if file contains long lines',
                    type=file, metavar='TEXFILE')

    return ap.parse_args()


def checker(content, maxlen):
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


# Find .tex files in folder srcdir.
# Returns:
# * texfiles: list, contains the relative paths to .tex files.
def find_texfiles(srcdir):
    texfiles = []

    for root, directories, files in os.walk(srcdir):
        for file in fnmatch.filter(files, '*.tex'):
            texfiles.append(os.path.join(root, file))

    return texfiles


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

    if args.check:
        content = args.check.readlines()
        checker(content, args.maxlen)
        sys.exit(0)

    script_path = os.path.dirname(os.path.abspath(__file__))
    command = ['python']
    command.append(os.path.join(script_path, 'breaklines.py'))
    command.append(str(args.maxlen))

    if args.srcdir:
        execute = confirm_srcdir()
        if not execute:
            print('Script aborted.')
            sys.exit(-1)

        texfiles = find_texfiles(args.srcdir)
        for file in texfiles:
            command.append(file)
            content = subprocess.check_output(command)
            command.pop()
            dump(content, file)
        sys.exit(0)

    if args.file:
        command.append(str(args.file.name))
        subprocess.call(command)
        sys.exit(0)

    print('\nScript is made to check users-guide repository for long lines.')
    print('Use -h or --help option to get more info.\n')


if __name__ == "__main__":
    main()
