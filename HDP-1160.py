#!/usr/bin/python

import os
import sys
import subprocess
import argparse

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


def main():
    args = get_input()

    if args.check:
        content = args.check.readlines()
        checker(content, args.maxlen)
        sys.exit(0)

    script_path = os.path.dirname(os.path.abspath(__file__))
    command = ['python']
    command.append(os.path.join(script_path, 'breaklines.py'))

    if args.srcdir:
        command.append(str(args.srcdir))
        command.append(str(args.maxlen))
        subprocess.call(command)
        sys.exit(0)

    if args.file:
        command.append(str(args.file.name))
        command.append(str(args.maxlen))
        subprocess.call(command)
        sys.exit(0)

    print('\nScript is made to check users-guide repository for long lines.')
    print('Use -h or --help option to get more info.\n')


if __name__ == "__main__":
    main()
