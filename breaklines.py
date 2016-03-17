#!/usr/bin/python

import re
import sys


# Global variables: command line arguments.
maxlen = int(sys.argv[1])
path = sys.argv[2]


# Read file from file's path.
def read_file(path):
    with open(path) as f:
        content = f.readlines()

    return content


# Build new file.
# Returns with a list, that represents the formatted file.
# Variables:
# * formatted: list, contains the formatted file.
# * cmd: int, stores depth of code blocks.
def format_file(content):
    # formatted will contain the formatted tex file.
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


# Param: line from file.
# Returns with the formatted line (inserted newline char).
# Variables:
# * processed: list, contains the formatted line
# * llen: int, line length
# * idx: int, actual char that is being examined
# * save: int, index of the character where newline char can be inserted
# * brackets: int, stores depth of curly brackets
# * comment: bool, 'True' if a line is a comment
# * num_of_indents: int, stores number of spaces at the beginning of the line
# * indentation: string, stores num_of_indents many spaces.
def split_line(line):
    global maxlen
    llen = len(line)

    # Early return: short line (less than maxlen)
    if llen <= maxlen:
        return line

    # Long line, process it.
    # Initializing variables.
    processed = []
    idx = save = brackets = 0
    comment = False

    # Check if line is indented.
    num_of_indents = check_indentation(line)

    # Search for insertion points
    while idx < llen:
        brackets += check_brackets(line[idx])
        brackets += check_exception(line, idx, brackets)

        if is_comment(line, idx):
            comment = True
        if is_insertion_possible(line[idx], brackets):
            save = idx

        idx += 1

        # Found an insertion point after indentation and
        # as close to maxlen as possible.
        if save > num_of_indents and idx >= maxlen:
            processed.extend(line[:save])
            processed.extend('\n')
            # Keep the next line indented.
            indentation = ' ' * num_of_indents
            # Decide if next line should be commented out from file.
            if comment:
                processed.extend(split_line('%' + indentation + line[save+1:]))
            else:
                processed.extend(split_line(indentation + line[save+1:]))
            return processed

    # No insertion point found, return with the line untouched.
    return line


# Check if character is a curly bracket.
# Returns:
# * -1 if entering bracket
# * 1 if closing bracket
# * 0 otherwise.
def check_brackets(c):
    if c == '{':
        return -1
    elif c == '}':
        return 1
    else:
        return 0


# Do not break line if represents a code.
# Returns:
# * -1 if entering codeblock
# * 1 if closing codeblock
# * 0 otherwise
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


# If { bracket is \hint{ or \samp{ do not mind it.
# If brackets var is above 0, then it is
# the \hint{ or \samp{ closing bracket.
def check_exception(line, idx, brackets):
    if line[idx-5:idx] == '\hint':
        return 1
    if line[idx-5:idx] == '\samp':
        return 1
    # Found a \hint or \samp closing '}' bracket.
    if brackets > 0:
        return -1

    return 0


# Check indentation of a line.
# Returns the number of spaces at the beginning of a line.
def check_indentation(line):
    idx = 0

    while (line[idx] == ' '):
        idx += 1

    return idx


# If line is comment, break it and insert %.
# Returns 'True' if there is a '%' without '\' behind it.
def is_comment(line, idx):
    return line[idx] == '%' and line[idx-1] != '\\'


# Check if we can insert \n at current character:
# Returns:
# * 'True', if character 'c' is space and brackets is zero.
# * 'False' otherwise.
def is_insertion_possible(c, brackets):
    return c == ' ' and brackets == 0


def main():
    content = read_file(path)
    newfile = format_file(content)
    print(''.join(newfile))


if __name__ == "__main__":
    main()
