#!/usr/bin/python

import re
import argparse

class prefix(object):
    item = '***\t'
    note = '[!]\t'


# Get input: source directory of users guide.
def get_input():
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--dryrun', help='check if file contains long lines',
                    action='store_true')
    ap.add_argument('-m', '--maxlen', help='the maximum length of a line '
                                           '(100 on default)',
                    type=int, default=100)
    ap.add_argument('texfile', help='the .tex file you want to check',
                    type=file)

    return ap.parse_args()


# Read .tex file.
def read_file(texfile):
    content = texfile.readlines()
    return content

def long_lines(content):
    maxlen = get_input().maxlen
    line_num = 1
    long_found = False

    for line in content:
        llen = len(line)
        if llen > maxlen:
            long_found = True
            print(prefix.item + 'LONG LINE on line ' + str(line_num))
        line_num += 1.

    if not long_found:
        print(prefix.note + 'There is no long lines in your file.')

# Build new file.
def format_file(content):

    # Var formatted will contain the formatted tex file.
    formatted = []
    # Do not insert newline char in code!
    cmd = 0

    for line in content:
        cmd += check_code(line)
        if cmd == 0:
            newline = split_line(line)
            formatted.extend(newline)
        else:
            formatted.extend(line)

    return formatted


# Insert newlines into long lines.
def split_line(line):
    maxlen = get_input().maxlen
    llen = len(line)

    # Short line, ignore it.
    if llen <= maxlen:
        return line

    # Long line, process it.
    # Initializing variables.
    processed = []
    idx = save = brackets = 0
    comment = False

    num_of_indents = check_indentation(line)
    # Search for insertion points
    while idx < llen:
        brackets += check_brackets(line[idx])
        brackets += check_exception(line, idx, brackets)
        if is_comment(line, idx):
            comment = True

        if (is_insertion_possible(line[idx], brackets)):
            save = idx

        idx += 1

        # Found an insertion point (before or after maxlen)
        if save > 0 and save > num_of_indents and idx >= maxlen:
            processed.extend(line[:save])
            processed.extend('\n')
            # Keep indentation
            indentation = ' ' * num_of_indents
            if comment:
                processed.extend(split_line('%' + indentation + line[save+1:]))
            else:
                processed.extend(split_line(indentation + line[save+1:]))
            return processed

    # No insertion point found
    return line


# Check if character is a curly bracket.
def check_brackets(c):
    if c == '{':
        return -1
    elif c == '}':
        return 1
    else:
        return 0


# Do not break line if represents a (partial) code.
def check_code(line):
    if re.match("(.*)\\\\begin{cmd}(.*)", line):
        return -1
    if re.match("(.*)\\\\end{cmd}(.*)", line):
        return 1
    if re.match("(.*)\\\\begin{code}(.*)", line):
        return -1
    if re.match("(.*)\\\\end{code}(.*)", line):
        return 1

    return 0


# if { bracket is \hint{, do not mind it.
def check_exception(line, idx, brackets):
    if line[idx-5:idx] == '\hint':
        return 1
    if line[idx-5:idx] == '\samp':
        return 1
 
    # Found a \hint or \samp closing '}' bracket.
    if brackets > 0:
        return -1
    return 0


# Check indentation of a line
def check_indentation(line):
    idx = 0
    while (line[idx] == ' ' and idx < 20):
        idx += 1

    return idx


# If line is comment, break it and insert %.
def is_comment(line, idx):
    return line[idx] == '%' and line[idx-1] != '\\'


# Check if we can insert \n at current character.
def is_insertion_possible(c, brackets):
    return c == ' ' and brackets == 0


# DEBUG: output content(param 1) into file(param 2)
def dump(content):
    print(''.join(content))


def main():
    args = get_input()
    content = read_file(args.texfile)
    if args.dryrun:
        msg = 'Searching for long lines in file: ' + str(args.texfile.name) + '\n'
        print('#' * len(msg))
        print(msg)
        long_lines(content)
        print('')
    else:
        newfile = format_file(content)
        dump(newfile)


if __name__ == "__main__":
    main()
