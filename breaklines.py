#!/usr/bin/python

import re
import sys
import fnmatch
import os

# Maximum length of a line
maxlen = int(sys.argv[2])


def read_file(file_path):
    with open(file_path) as f:
        content = f.readlines()
    return content


# Find .tex files in root folder.
def find(srcdir):
    texfiles = []
    for root, directories, files in os.walk(srcdir):
        for file in fnmatch.filter(files, '*.tex'):
            texfiles.append(os.path.join(root, file))

    return texfiles


# Build new file.
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


# Insert newlines into long lines.
def split_line(line):
    global maxlen
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


# If { bracket is \hint{, do not mind it.
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
    while (line[idx] == ' '):
        idx += 1

    return idx


# If line is comment, break it and insert %.
def is_comment(line, idx):
    return line[idx] == '%' and line[idx-1] != '\\'


# Check if we can insert \n at current character.
def is_insertion_possible(c, brackets):
    return c == ' ' and brackets == 0


# DEBUG: output content(param 1) into file(param 2)
def dump(content, file):
    f = open(file, 'w')
    for line in content:
        f.write(line)
    f.close()


def main():
    file_path = sys.argv[1]

    if len(sys.argv) > 3:
        if sys.argv[3] == 'dir':
            print('WARNING: This command will overwrite every .tex file in your directory')
            user_input = raw_input('Continue? [yes/NO]: ')
            execute = False
            if str(user_input) == 'yes':
                execute = True
            if not execute:
                print('Aborted.')
                sys.exit(0)

            srcdir = sys.argv[1]
            files = find(srcdir)
            for file in files:
                print('Processing file: ' + file)
                content = read_file(file)
                newfile = format_file(content)
                dump(newfile, file)
                print('Formatted file: ' + file)
            print("PROGRAM ENDS.")
    else:
        content = read_file(file_path)
        newfile = format_file(content)
        print(''.join(newfile))

if __name__ == "__main__":
    main()
