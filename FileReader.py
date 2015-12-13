#!/usr/bin/python


def read_file(fname):
    with open(fname) as f:
        #content = f.readlines()
        content = [line.rstrip('\n') for line in f]

    return content
