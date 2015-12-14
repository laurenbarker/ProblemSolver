#!/usr/bin/python


def read_file(fname):
    with open(fname) as f:
        content = [line.rstrip('\n') for line in f]

    longest_line = content[0]

    for line in content:
        if len(line) > len(longest_line):
            longest_line = line

    for idx, line in enumerate(content):
        while len(line) < len(longest_line):
            line = line + ' '
        content[idx] = line

    return content
